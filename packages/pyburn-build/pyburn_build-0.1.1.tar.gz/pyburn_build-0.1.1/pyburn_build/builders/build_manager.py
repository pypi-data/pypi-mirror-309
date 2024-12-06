from typing import Union
from loguru import logger
from pyburn_build.config.project_config import ProjectConfig
from pyburn_build.config.toolchain_config import ToolchainConfig
from pyburn_build.config.toolchain_config import TargetData
from pyburn_build.builders.builders import CBuilder, CPPBuilder, CustomBuilder


def get_builder(project_config: ProjectConfig, compiler_name: str, target: TargetData):
	compiler_name = compiler_name.lower()

	if compiler_name == "gcc" or compiler_name == "clang":
		return CBuilder(project_config, compiler_name, target)
	elif compiler_name == "g++" or compiler_name == "clang++":
		return CPPBuilder(project_config, compiler_name, target)
	else:
		return CustomBuilder(project_config, compiler_name, target)


class BuildManager:
	"""
	This class describes a build manager.
	"""

	def __init__(
		self, project_config: ProjectConfig, toolchain_config: ToolchainConfig
	):
		"""
		Constructs a new instance.

		:param		project_config:	   The project configuration
		:type		project_config:	   ProjectConfig
		:param		toolchain_config:  The toolchain configuration
		:type		toolchain_config:  ToolchainConfig
		"""
		self.project_config = project_config
		self.toolchain_config = toolchain_config

		self.default_compiler = self.project_config.COMPILER_NAME
		self.language = self.project_config.LANGUAGE

		self.supported_compilers = ["gcc", "g++", "clang", "clang++"]

	def build(self, targets: Union[list, str]):
		"""
		Build project

		:param		targets:  The targets
		:type		targets:  { type_description }
		"""
		logger.info(f'{"=" * 16} Start build (targets: {targets})')
		for target in self.toolchain_config.targets:
			if targets == "all" or target in targets:
				logger.debug(f'{"=" * 8} Start Build Target {target.name}')
				compiler = (
					target.compiler
					if target.compiler is not None
					else self.default_compiler
				)

				if compiler.lower() not in self.supported_compilers:
					logger.warn("Compiler not supported, using CustomBuilder...")

				builder = get_builder(self.project_config, compiler, target)
				builder.execute_commands(self.toolchain_config.prelude_commands)
				builder.run()
				builder.execute_commands(self.toolchain_config.post_commands)
				logger.debug(f'[cyan]{"=" * 8}[/cyan] End Build Target {target.name}')
			else:
				logger.debug(f"Skip target: {target.name}")
