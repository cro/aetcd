from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        build_data["dependencies"] = ["grpcio", "grpcio-tools"]
        # Example: Run a shell command before building
        subprocess.run(["python", "-m", "grpc_tools.protoc", "-Iproto", "--python_out=aetcd/rpc/", "--grpc_python_out=aetcd/rpc/", "proto/rpc.proto", "proto/auth.proto", "proto/kv.proto"], check=True)
        subprocess.run(["sed", "-i", "-e", "s/import auth_pb2/from . import auth_pb2/g", "aetcd/rpc/rpc_pb2.py"], check=True)
        subprocess.run(["sed","-i","-e","s/import kv_pb2/from . import kv_pb2/g","aetcd/rpc/rpc_pb2.py"], check=True)
        subprocess.run(["sed","-i","-e","s/import rpc_pb2/from . import rpc_pb2/g", "aetcd/rpc/rpc_pb2_grpc.py"], check=True)

        # Add compiled files to build
        build_data["artifacts"] = ["aetcd/rpc/*.py"]
