from __future__ import annotations
import enum
import os
from types import ModuleType
from typing import Any, Callable, TYPE_CHECKING, List, Union
from .storage import (
    DatabaseInfo,
    ConnectionInfo,
    DbReader,
    DbWriter,
    MemoryReader,
    MemoryWriter,
    TempCollection,
)
import inspect
from pymongo.database import Database as MongoDatabase

# todo replace print with logging
class ProcessorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Project:
    modules: dict[str, Module]
    _debug_db: DatabaseInfo
    _debug_env_params: dict

    def __init__(self, name):
        self.modules = {}
        self._debug_db = None
        self._debug_env_params = None
        self.name = name

    def set_connection(self, connection_string: str, database_name: str):
        self._debug_db = DatabaseInfo(database_name, ConnectionInfo(connection_string))

    def _get_debug_db(self):
        return self._debug_db
    
    def set_env_params(self, value: dict):
        self._debug_env_params = value
    
    def _get_debug_env_params(self):
        return self._debug_env_params

    def add_module(self, module: Module):
        if module.name in self.modules:
            raise Exception(f"duplicated module name '{module.name}'")
        self.modules[module.name] = module
        module.project = self

    def get_module(self, info: str | ModuleType):
        if isinstance(info, str):
            name = info
        else:
            parts = info.__name__.split(".")
            name = ".".join(parts[1:])
        if name not in self.modules:
            raise Exception(f"module '{name}' is not defined")
        return self.modules[name]

    def add_modules(self, modules: list[Module]):
        for item in modules:
            self.add_module(item)


class Port:
    def __init__(
        self,
        name: str,
        title: str = None,
        description: str = None,
        default_binding: str = None,
        read_only: bool = False,
        schema: Any = None,
        collection_type: CollectionType = None
    ):
        self.name = name
        self.title = title
        self.description = description
        self.default_binding = default_binding
        self.read_only = read_only
        self.schema = schema
        self.collection_type = collection_type


def _default_action(params: Task):
    print(f"Processor {params.processor.name} has no action defined")


def _get_source_file_name():
    caller_frame = inspect.stack()[2]
    return (
        caller_frame.filename
        # .replace(os.getcwd(), "")
        .replace("\\", "/")
        # .rstrip("/")[1:]
    )


def _get_module_name_from_path(path: str):
    # TODO усовершенствовать убрать хардкод
    rel_path = path.split("processors/")[1].lower()
    rel_path = rel_path.replace("/__init__.py", "").replace(".py", "")
    rel_path = rel_path.replace("/", ".")
    return rel_path


def _get_processor_name_from_path(path):
    return path.rsplit("/", 1)[-1].split(".", 1)[0]


class Module:
    project: Project

    def __init__(self, name: str = None):
        self.defined_in_file = _get_source_file_name()
        if name == None:
            name = _get_module_name_from_path(self.defined_in_file)
        self.name = name
        self.processors = dict[str, Processor]()
        self.project = None

    def add_processor(self, processor: Processor):
        if processor.name in self.processors:
            raise Exception(f"duplicated processor name '{processor.name}'")
        self.processors[processor.name] = processor
        processor.module = self

    def add_processors(self, processors: list[Processor]):
        for processor in processors:
            self.add_processor(processor)

    def get_processor(self, info: str | ModuleType):
        name = ""
        if isinstance(info, str):
            name = info
        else:
            name = info.__name__.rsplit(".", 1)[-1]
        if name not in self.processors:
            raise Exception(f"processor '{name}' is not defined")
        return self.processors[name]

    def create_task(self, processor_info: str | ModuleType):
        return self.get_processor(processor_info).create_task()

class CollectionType(enum.Enum):
    COMPARISON_REPORT = "COMPARISON_REPORT"

class Processor:
    module: Module

    def __init__(self, title: str = None, description: str = None, name: str = None):
        self.defined_in_file = _get_source_file_name()
        if name == None:
            name = _get_processor_name_from_path(self.defined_in_file)
        self.name = name
        self.title = title
        self.description = description
        self.inputs = dict[str, Port]()
        self.outputs = dict[str, Port]()
        self.action = _default_action
        self.module = None

    def add_input(
        self,
        name: str,
        title: str = None,
        description: str = None,
        schema: dict[str, Any] = None,
        default_binding: str = None,
        read_only: bool = False,
    ):
        item = Port(name, title, description, default_binding, read_only, schema)
        if name in self.inputs:
            raise Exception(f"duplicated input name {name} in processor {self.name}")
        self.inputs[name] = item

    def add_output(
        self,
        name: str,
        title: str = None,
        description: str = None,
        schema: dict[str, Any] = None,
        default_binding: str = None,
        read_only: bool = False,
        collection_type: CollectionType = None
    ):
        item = Port(name, title, description, default_binding, read_only, schema,collection_type)
        if name in self.outputs:
            raise Exception(f"duplicated output name {name} in processor {self.name}")
        self.outputs[name] = item

    def add_default_input(
        self,
        title: str = "Вход",
        description: str = None,
        schema: dict[str, Any] = None,
        default_binding: str = None,
        read_only: bool = False,
    ):
        self.add_input(
            "default", title, description, schema, default_binding, read_only
        )

    def add_params_input(
        self,
        title: str = "Параметры",
        description: str = None,
        schema: dict[str, Any] = None,
    ):
        self.add_input("params", title, description, schema)

    def add_default_output(
        self,
        title: str = "Выход",
        description: str = None,
        schema: dict[str, Any] = None,
        default_binding: str = None,
        read_only: bool = False,
        collection_type: CollectionType = None
    ):
        self.add_output(
            "default", title, description, schema, default_binding, read_only, collection_type
        )

    def set_action(self, action: Callable[[str], None]):
        self.action = action

    def create_task(self) -> Task:
        return Task(self)


class Task:
    _database: DatabaseInfo
    _env_params: dict

    def __init__(self, processor: Processor):
        self.processor = processor
        self._input_binding = dict[str, str | list[dict[str, Any]] | dict[str, Any]]()
        self._output_binding = dict[str, str | str | list[dict[str, Any]]]()
        self._writers = dict[str, DbWriter | MemoryWriter]()
        self._readers = dict[str, DbReader | MemoryReader]()
        self._database = None
        self._env_params = None

    # Config

    def _remove_input_binging(self, name: str):
        if name in self._input_binding:
            del self._input_binding[name]

    def _remove_output_binging(self, name: str):
        if name in self._output_binding:
            del self._output_binding[name]

    def bind_input(
        self, input_name: str, source: list[dict[str, Any]] | dict[str, Any] | str
    ):
        self._remove_input_binging(input_name)
        if not input_name in self.processor.inputs:
            raise Exception(f"Input '{input_name}' is not declared")
        if isinstance(source, list):
            source = source.copy()
        self._input_binding[input_name] = source

    def bind_output(self, output_name: str, target: list[dict[str, Any]] | str):
        self._remove_output_binging(output_name)
        if not output_name in self.processor.outputs:
            raise Exception(f"Output '{output_name}' is not declared")
        self._output_binding[output_name] = target

    def bind_params(self, source: list[dict[str, Any]] | dict[str, Any] | str):
        self.bind_input("params", source)

    def bind_default_input(self, source: list[dict[str, Any]] | dict[str, Any] | str):
        self.bind_input("default", source)

    def bind_default_output(self, target: list[dict[str, Any]] | str):
        self.bind_output("default", target)

    def bind_inputs(
        self,
        input_bindings: dict[str, Union[str, List[dict[str, Any]], dict[str, Any]]],
    ):
        for name in input_bindings:
            self.bind_input(name, input_bindings[name])

    def bind_outputs(
        self, output_bindings: dict[str, Union[str, List[dict[str, Any]]]]
    ):
        for name in output_bindings:
            self.bind_output(name, output_bindings[name])

    def _print_bindings(self, ports: dict, bindings: dict):
        for name in ports:
            val = None
            if name in bindings:
                val = bindings[name]
            text = ""
            if val == None:
                text = "null"
            elif isinstance(val, str):
                text = val
            elif isinstance(val, dict):
                text = str(val)
            else:
                text = "list[]"
            print("- " + name + ": " + text)

    def _apply_default_binding(self):
        def apply(ports: dict[str, Port], bindings: dict, type: str):
            for name in ports:
                if name not in bindings:
                    port = ports[name]
                    if port.default_binding != None:
                        bindings[name] = port.default_binding
                    else:
                        raise Exception(
                            f"Processor '{self.processor.name}' {type} port '{name}' is not bound"
                        )

            for name in bindings:
                if name not in ports:
                    raise Exception(
                        f"Invalid binding. Processor '{self.processor.name}' does not contain {type} '{name}'"
                    )

        apply(self.processor.inputs, self._input_binding, "input")
        apply(self.processor.outputs, self._output_binding, "output")

    def get_input_binding_info(self):
        return self._input_binding.copy()

    def get_output_binding_info(self):
        return self._output_binding.copy()

    def prepare(self):
        self._apply_default_binding()

    def run(self):
        print("")
        print(f"Start processor '{self.processor.name}' task")
        self.prepare()
        print("input binding")
        self._print_bindings(self.processor.inputs, self._input_binding)
        print("")
        print("output binding")
        self._print_bindings(self.processor.outputs, self._output_binding)
        print("")
        task_context = self  # TaskContext(self)
        self.processor.action(task_context)
        for name in task_context._writers:
            if not task_context._writers[name].is_closed():
                raise Exception(
                    f"Writer '{name}' in processor '{self.processor.name}' was not closed. Use writer.close() when writing is finished"
                )

        print(f"Processor '{self.processor.name}' task finished")
        print("")

    def get_input_count(self, name):
        if name not in self._readers:
            self.get_reader(name)
        return self._readers[name].get_count()

    def get_output_count(self, name):
        if name not in self._writers:
            return 0
        return self._writers[name].get_count()

    # Exec

    def set_connection(self, connection_string: str, database_name: str):
        self._database = DatabaseInfo(database_name, ConnectionInfo(connection_string))

    def _get_database(self):
        if self._database != None:
            return self._database
        return self.processor.module.project._get_debug_db()

    def set_database(self, value: MongoDatabase):
        self._database = DatabaseInfo(instance=value)

    def set_env_params(self, value: dict):
        self._env_params = value

    def get_env_params(self):
        if self._env_params != None:
            return self._env_params
        return self.processor.module.project._get_debug_env_params()

    def temp_coll(self, name):
        # todo учесть контекст чтобы не затереть данные при параллельном выполнении, и при этом не накапливать неконтролируемо временные данные в БД
        full_name = f"sys_qs_flow_{name}"
        return TempCollection(full_name, self._get_database())

    def get_reader(self, input_name: str) -> DbReader | MemoryReader:
        if not input_name in self.processor.inputs:
            raise Exception(f"Input '{input_name}' is not declared")
        source = self._input_binding[input_name]
        if isinstance(source, str):
            val = DbReader(source, self._get_database())
        else:
            if isinstance(source, dict):
                source = [source]
            val = MemoryReader(source, self.processor.inputs[input_name].schema)
        self._readers[input_name] = val
        return val

    def get_writer(self, output_name: str) -> DbWriter:
        if not output_name in self.processor.outputs:
            raise Exception(f"Output '{output_name}' is not declared")
        target = self._output_binding[output_name]
        if not output_name in self._writers:
            if isinstance(target, str):
                val = DbWriter(target, self._get_database())
            else:
                if isinstance(target, dict):
                    target = [target]
                val = MemoryWriter(target)
            self._writers[output_name] = val
        return self._writers[output_name]

    def get_default_reader(self) -> DbReader | MemoryReader:
        return self.get_reader("default")

    def get_params_reader(self) -> DbReader | MemoryReader:
        return self.get_reader("params")

    def get_default_writer(self) -> DbWriter:
        return self.get_writer("default")


# class TaskContext:
#     def __init__(self, task: Task):
#         self.task = task
#         self._writers = dict[str, DbWriter | MemoryWriter]()
