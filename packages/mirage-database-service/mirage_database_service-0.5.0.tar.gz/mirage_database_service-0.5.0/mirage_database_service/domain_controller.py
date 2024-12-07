import consul
from flask import Flask, request, jsonify
import importlib
import logging
import inspect
from typing import get_type_hints
import os

class RequestDataPacket:
    def __init__(self, schema, old_data, new_data, patch):
        self.schema = schema
        self.old_data = old_data
        self.new_data = new_data
        self.patch = patch


class ValidationResult:
    def __init__(self, status, message = None):
        self.status = status
        self.message = message

    def to_json(self):
        return {
            "status": self.status,
            "message": self.message
        }

class ControllerOptions:
    def __init__(self, service_name, service_id, port, ip_address, consul_host, consul_port, consul_schema):
        self.service_name = service_name
        self.service_id = service_id
        self.port = port
        self.ip_address = ip_address
        self.consul_host = consul_host
        self.consul_port = consul_port
        self.consul_schema = consul_schema


def controller_options_factory(service_name = "MyService",
                               service_id = "MyService-1",
                               address="localhost",
                               port=5000,
                               consul_url = "localhost",
                               consul_schema = "http",
                               consult_port = 8500)->ControllerOptions:
    consul_url = os.getenv('CONSUL_URL', consul_url)
    consul_schema = os.getenv('CONSUL_SCHEMA', consul_schema)
    consul_port = int(os.getenv('CONSUL_PORT', consult_port))
    domainName = os.getenv('DOMAIN_NAME', service_name)
    service_id = os.getenv('SERVICE_ID', service_id)
    ip_address = os.getenv('IP_ADDRESS', address)
    port = int(os.getenv('PORT', port))
    return ControllerOptions(service_name=domainName, service_id=service_id, port=port, ip_address=ip_address,
                             consul_host=consul_url, consul_port=consul_port, consul_schema=consul_schema)



# Define a custom trace level
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

# Add a trace method to the logger
def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)

logging.Logger.trace = trace

# Configure the logging format and level
logging.basicConfig(
    level=TRACE_LEVEL,  # Set the lowest logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class RystadEnergyDomainController:
    def __init__(self, options: ControllerOptions):
        self.logger = logging.getLogger(f"{options.service_name}Controller")
        self.logger.trace(f"Initializing RigCubeApp with service_name={options.service_name}, service_id={options.service_id}, port={options.port}")
        self.app = Flask(__name__)
        self.service_name = options.service_name
        self.service_id = options.service_id
        self.port = options.port
        self.consul_host = options.consul_host
        self.consult_port = options.consul_port
        self.consul_schema = options.consul_schema
        self.ip_address = options.ip_address

        # Register default routes
        self.register_routes()

        # Register the service with Consul
        self.register_service()
        self.module_cache = {}

    def register_service(self):
        self.logger.trace("Registering service with Consul")
        client = consul.Consul(host=self.consul_host, port=self.consult_port, scheme=self.consul_schema)

        # Register the service with health check

        client.agent.service.register(
            name=self.service_name,
            service_id=self.service_id,
            address=self.ip_address,
            port=self.port,
            tags=["validation", "preprocessing", "postprocessing"],
            check={
                "http": f"http://{self.ip_address}:{self.port}/health",
                "interval": "10s",
                "timeout": "1s"
            }
        )

        self.logger.info(f"Service '{self.service_name}' registered successfully at '{self.ip_address}':'{self.port}'")


    def register_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy"}), 200

        @self.app.route('/validation', methods=['PUT'])
        def validate():
            self.logger.trace("Validation endpoint called with data: %s", request.json)
            data = request.json
            action = data["Action"]
            request_data = RequestDataPacket(
                schema=data["Schema"],
                old_data=data["OldData"],
                new_data=data["NewData"],
                patch=data["Patch"]
            )

            entity = request_data.schema["Name"]
            root_path = os.getcwd()
            module_path = os.path.join(root_path, 'validations', entity + '.py')
            if module_path in self.module_cache:
                module = self.module_cache[module_path]
            else:
                try:
                    spec = importlib.util.spec_from_file_location(entity, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.module_cache[module_path] = module
                except (FileNotFoundError, ImportError):
                    self.logger.info("No module named %s. Not validated", module_path)
                    return jsonify({"status": "Valid"}), 200

            action_method_map = {
                0: "on_create",
                1: "on_update",
                2: "on_delete"
            }

            method_name = action_method_map.get(action)
            if not method_name:
                self.logger.error(f"Invalid action: {action}")
                return jsonify({"status": "Invalid", "message": f"Invalid action: {action}"}), 400

            if hasattr(module, method_name):
                method_func = getattr(module, method_name)
                type_hints = get_type_hints(method_func)
                if 'return' in type_hints and type_hints['return'] == ValidationResult:
                    sig = inspect.signature(method_func)
                    params = list(sig.parameters.values())
                    if len(params) == 1 and params[0].annotation == RequestDataPacket:
                        validation_result = method_func(request_data)
                        self.logger.trace("Validation result: %s", validation_result.to_json())
                        return jsonify(validation_result.to_json())
                    else:
                        self.logger.error(f"Method {method_name} does not accept the required parameter type")
                        return jsonify({"status": "Invalid",
                                        "message": f"Method {method_name} does not accept the required parameter type"}), 400
                else:
                    self.logger.error(f"Method {method_name} does not return ValidationResult")
                    return jsonify({"status": "Invalid",
                                    "message": f"Method {method_name} does not return ValidationResult"}), 400
            else:
                self.logger.error(f"Required method {method_name} is missing in the module")
                return jsonify({"status": "Invalid", "message": f"Required method {method_name} is missing"}), 400

        @self.app.route('/preprocess', methods=['PUT'])
        def preprocess():
            data = request.json
            schema = data["Schema"]
            old_data = data["OldData"]
            new_data = data["NewData"]
            patch = data["Patch"]
            action = data["Action"]

            # Add processing logic here
            return jsonify({"status": "preprocessed"}), 200

        @self.app.route('/postprocess', methods=['PUT'])
        def postprocess():
            data = request.json
            schema = data["Schema"]
            old_data = data["OldData"]
            new_data = data["NewData"]
            patch = data["Patch"]
            action = data["Action"]

            # Add postprocessing logic here
            return jsonify({"status": "postprocessed"}), 200

    def add_route(self, route, view_func, methods=['GET']):
        """Allows adding custom routes dynamically."""
        self.app.add_url_rule(route, view_func=view_func, methods=methods)