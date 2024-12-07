"""This class is used to generate a study (along with the corresponding tree) from a parameter file,
and potentially a set of template files.

This class makes use of "eval", which is known to be a security risk. ast.literal_eval can't be
used here because variables from a specified namespace are being passed to the eval function.
The use of eval is justified here because the input is controlled by the user only through the
configuration file. If the user wants to write an unsafe expression, it's their responsibility.
"""

# ==================================================================================================
# --- Imports
# ==================================================================================================

# Import standard library modules
import copy
import inspect
import itertools
import logging
import os
import shutil
from typing import Any, Optional

# Import third-party modules
import numpy as np
import ruamel.yaml as yaml
from black import FileMode, format_str
from jinja2 import Environment, FileSystemLoader

# Import user-defined modules
from study_da.utils import clean_dic, load_dic_from_path, nested_set

from .parameter_space import (
    convert_for_subvariables,
    linspace,
    list_values_path,
    logspace,
)


# ==================================================================================================
# --- Class definition
# ==================================================================================================
class GenerateScan:
    """
    A class to generate a study (along with the corresponding tree) from a parameter file,
    and potentially a set of template files.

    Attributes:
        config (dict): The configuration dictionary.
        ryaml (yaml.YAML): The YAML parser.
        dic_common_parameters (dict): Dictionary of common parameters across generations.

    Methods:
        __init__(): Initializes the generation scan with a configuration file or dictionary.
        render(): Renders the study file using a template.
        write(): Writes the study file to disk.
        generate_render_write(): Generates, renders, and writes the study file.
        get_dic_parametric_scans(): Retrieves dictionaries of parametric scan values.
        parse_parameter_space(): Parses the parameter space for a given parameter.
        browse_and_collect_parameter_space(): Browses and collects the parameter space for a given
            generation.
        postprocess_parameter_lists(): Postprocesses the parameter lists.
        create_scans(): Creates study files for parametric scans.
        complete_tree(): Completes the tree structure of the study dictionary.
        write_tree(): Writes the study tree structure to a YAML file.
        create_study_for_current_gen(): Creates study files for the current generation.
        create_study(): Creates study files for the entire study.
        eval_conditions(): Evaluates the conditions to filter out some parameter values.
        filter_for_concomitant_parameters(): Filters the conditions for concomitant parameters.
    """

    def __init__(
        self, path_config: Optional[str] = None, dic_scan: Optional[dict[str, Any]] = None
    ):  # sourcery skip: remove-redundant-if
        """
        Initialize the generation scan with a configuration file or dictionary.

        Args:
            path_config (Optional[str]): Path to the configuration file for the scan.
                Default is None.
            dic_scan (Optional[dict[str, Any]]): Dictionary containing the scan configuration.
                Default is None.

        Raises:
            ValueError: If neither or both of `path_config` and `dic_scan` are provided.
        """
        # Load the study configuration from file or dictionary
        if dic_scan is None and path_config is None:
            raise ValueError(
                "Either a path to the configuration file or a dictionary must be provided."
            )
        elif dic_scan is not None and path_config is not None:
            raise ValueError("Only one of the configuration file or dictionary must be provided.")
        elif path_config is not None:
            self.config, self.ryaml = load_dic_from_path(path_config)
        elif dic_scan is not None:
            self.config = dic_scan
            self.ryaml = yaml.YAML()
        else:
            raise ValueError("An unexpected error occurred.")

        # Parameters common across all generations (e.g. for parallelization)
        self.dic_common_parameters: dict[str, Any] = {}

        # Path to the tree file
        self.path_tree = self.config["name"] + "/" + "tree.yaml"

    def render(
        self,
        str_parameters: str,
        template_path: str,
        path_main_configuration: str,
        study_path: Optional[str] = None,
        str_dependencies: Optional[dict[str, str]] = None,
    ) -> str:
        """
        Renders the study file using a template.

        Args:
            str_parameters (str): The string representation of parameters to declare/mutate.
            template_path (str): The path to the template file.
            path_main_configuration (str): The path to the main configuration file.
            study_path (str, optional): The path to the root of the study. Defaults to None.
            dependencies (dict[str, str], optional): The dictionary of dependencies. Defaults to {}.

        Returns:
            str: The rendered study file.
        """

        # Handle mutable default argument
        if str_dependencies is None:
            dependencies = ""
        if study_path is None:
            study_path = ""

        # Generate generations from template
        directory_path = os.path.dirname(template_path)
        template_name = os.path.basename(template_path)
        environment = Environment(
            loader=FileSystemLoader(directory_path),
            variable_start_string="{}  ###---",
            variable_end_string="---###",
        )
        template = environment.get_template(template_name)

        # Better not to render the dependencies path this way, as it becomes too cumbersome to
        # handle the paths when using clusters

        return template.render(
            parameters=str_parameters,
            main_configuration=path_main_configuration,
            path_root_study=study_path,
            # dependencies = str_dependencies,
        )

    def write(self, study_str: str, file_path: str, format_with_black: bool = True):
        """
        Writes the study file to disk.

        Args:
            study_str (str): The study file string.
            file_path (str): The path to write the study file.
            format_with_black (bool, optional): Whether to format the output file with black.
                Defaults to True.
        """

        # Format the string with black
        if format_with_black:
            study_str = format_str(study_str, mode=FileMode())

        # Make folder if it doesn't exist
        folder = os.path.dirname(file_path)
        if folder != "":
            os.makedirs(folder, exist_ok=True)

        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(study_str)

    def generate_render_write(
        self,
        gen_name: str,
        job_directory_path: str,
        template_path: str,
        depth_gen: int,
        dic_mutated_parameters: dict[str, Any] = {},
    ) -> list[str]:  # sourcery skip: default-mutable-arg
        """
        Generates, renders, and writes the study file.

        Args:
            gen_name (str): The name of the generation.
            study_path (str): The path to the job folder.
            template_path (str): The path to the template folder.
            depth_gen (int): The depth of the generation in the tree.
            dic_mutated_parameters (dict[str, Any], optional): The dictionary of mutated parameters.
                Defaults to {}.

        Returns:
            tuple[str, list[str]]: The study file string and the list of study paths.
        """

        directory_path_gen = f"{job_directory_path}"
        if not directory_path_gen.endswith("/"):
            directory_path_gen += "/"
        file_path_gen = f"{directory_path_gen}{gen_name}.py"
        logging.info(f'Now rendering generation "{file_path_gen}"')

        # Generate the string of parameters
        str_parameters = "{"
        for key, value in dic_mutated_parameters.items():
            if isinstance(value, str):
                str_parameters += f"'{key}' : '{value}', "
            else:
                str_parameters += f"'{key}' : {value}, "
        str_parameters += "}"

        # Adapt the dict of dependencies to the current generation
        dic_dependencies = self.config["dependencies"] if "dependencies" in self.config else {}

        # Unpacking list of dependencies
        dic_dependencies = {
            **{
                key: value for key, value in dic_dependencies.items() if not isinstance(value, list)
            },
            **{
                f"{key}_{str(i).zfill(len(str(len(value))))}": i_value
                for key, value in dic_dependencies.items()
                if isinstance(value, list)
                for i, i_value in enumerate(value)
            },
        }
        self.config["dependencies"] = dic_dependencies

        # Initial dependencies are always copied at the root of the study (hence value.split("/")[-1])
        dic_dependencies = {
            key: "../" * depth_gen + value.split("/")[-1] for key, value in dic_dependencies.items()
        }

        # Always load configuration from above generation, and remove the path from dependencies
        path_main_configuration = "../" + dic_dependencies.pop("main_configuration").split("/")[-1]

        # Create the str for the dependencies
        str_dependencies = "{"
        for key, value in dic_dependencies.items():
            str_dependencies += f"'{key}' : '{value}', "
        str_dependencies += "}"

        # Render and write the study file
        study_str = self.render(
            str_parameters,
            template_path=template_path,
            path_main_configuration=path_main_configuration,
            study_path=os.path.abspath(self.config["name"]),
            str_dependencies=str_dependencies,
        )

        self.write(study_str, file_path_gen)
        return [directory_path_gen]

    def get_dic_parametric_scans(
        self, generation: str
    ) -> tuple[dict[str, Any], dict[str, Any], np.ndarray | None]:
        """
        Retrieves dictionaries of parametric scan values.

        Args:
            generation: The generation name.

        Returns:
            tuple[dict[str, Any], dict[str, Any], np.ndarray|None]: The dictionaries of parametric
                scan values, another dictionnary with better naming for the tree creation, and an
                array of conditions to filter out some parameter values.
        """

        if generation == "base":
            raise ValueError("Generation 'base' should not have scans.")

        # Remember common parameters as they might be used across generations
        if "common_parameters" in self.config["structure"][generation]:
            self.dic_common_parameters[generation] = {}
            for parameter in self.config["structure"][generation]["common_parameters"]:
                self.dic_common_parameters[generation][parameter] = self.config["structure"][
                    generation
                ]["common_parameters"][parameter]

        # Check that the generation has scans
        if (
            "scans" not in self.config["structure"][generation]
            or self.config["structure"][generation]["scans"] is None
        ):
            dic_parameter_lists = {"": [generation]}
            dic_parameter_lists_for_naming = {"": [generation]}
            array_conditions = None
            ll_concomitant_parameters = []
        else:
            # Browse and collect the parameter space for the generation
            (
                dic_parameter_lists,
                dic_parameter_lists_for_naming,
                dic_subvariables,
                ll_concomitant_parameters,
                l_conditions,
            ) = self.browse_and_collect_parameter_space(generation)

            # Get the dimension corresponding to each parameter
            dic_dimension_indices = {
                parameter: idx for idx, parameter in enumerate(dic_parameter_lists)
            }

            # Generate array of conditions to filter out some of the values later
            # Is an array of True values if no conditions are present
            array_conditions = self.eval_conditions(l_conditions, dic_parameter_lists)

            # Filter for concomitant parameters
            array_conditions = self.filter_for_concomitant_parameters(
                array_conditions, ll_concomitant_parameters, dic_dimension_indices
            )

            # Postprocess the parameter lists and update the dictionaries
            dic_parameter_lists, dic_parameter_lists_for_naming = self.postprocess_parameter_lists(
                dic_parameter_lists, dic_parameter_lists_for_naming, dic_subvariables
            )

        return (
            dic_parameter_lists,
            dic_parameter_lists_for_naming,
            array_conditions,
        )

    def parse_parameter_space(
        self,
        parameter: str,
        dic_curr_parameter: dict[str, Any],
        dic_parameter_lists: dict[str, Any],
        dic_parameter_lists_for_naming: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Parses the parameter space for a given parameter.

        Args:
            parameter (str): The parameter name.
            dic_curr_parameter (dict[str, Any]): The dictionary of current parameter values.
            dic_parameter_lists (dict[str, Any]): The dictionary of parameter lists.
            dic_parameter_lists_for_naming (dict[str, Any]): The dictionary of parameter lists for naming.

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: The updated dictionaries of parameter lists.
        """

        if "linspace" in dic_curr_parameter:
            parameter_list = linspace(dic_curr_parameter["linspace"])
            dic_parameter_lists_for_naming[parameter] = parameter_list
        elif "logspace" in dic_curr_parameter:
            parameter_list = logspace(dic_curr_parameter["logspace"])
            dic_parameter_lists_for_naming[parameter] = parameter_list
        elif "path_list" in dic_curr_parameter:
            l_values_path_list = dic_curr_parameter["path_list"]
            parameter_list = list_values_path(l_values_path_list, self.dic_common_parameters)
            dic_parameter_lists_for_naming[parameter] = [
                f"{n:02d}" for n, path in enumerate(parameter_list)
            ]
        elif "list" in dic_curr_parameter:
            parameter_list = dic_curr_parameter["list"]
            dic_parameter_lists_for_naming[parameter] = parameter_list
        elif "expression" in dic_curr_parameter:
            parameter_list = np.round(
                eval(dic_curr_parameter["expression"], copy.deepcopy(dic_parameter_lists)),
                8,
            )
            dic_parameter_lists_for_naming[parameter] = parameter_list
        else:
            raise ValueError(f"Scanning method for parameter {parameter} is not recognized.")

        dic_parameter_lists[parameter] = np.array(parameter_list)
        return dic_parameter_lists, dic_parameter_lists_for_naming

    def browse_and_collect_parameter_space(
        self,
        generation: str,
    ) -> tuple[
        dict[str, Any],
        dict[str, Any],
        dict[str, Any],
        list[list[str]],
        list[str],
    ]:
        """
        Browses and collects the parameter space for a given generation.

        Args:
            generation (str): The generation name.

        Returns:
            tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[list[str]]]: The updated
                dictionaries of parameter lists.
        """

        l_conditions = []
        ll_concomitant_parameters = []
        dic_subvariables = {}
        dic_parameter_lists = {}
        dic_parameter_lists_for_naming = {}
        for parameter in self.config["structure"][generation]["scans"]:
            dic_curr_parameter = self.config["structure"][generation]["scans"][parameter]

            # Parse the parameter space
            dic_parameter_lists, dic_parameter_lists_for_naming = self.parse_parameter_space(
                parameter, dic_curr_parameter, dic_parameter_lists, dic_parameter_lists_for_naming
            )

            # Store potential subvariables
            if "subvariables" in dic_curr_parameter:
                dic_subvariables[parameter] = dic_curr_parameter["subvariables"]

            # Save the condition if it exists
            if "condition" in dic_curr_parameter:
                l_conditions.append(dic_curr_parameter["condition"])

            # Save the concomitant parameters if they exist
            if "concomitant" in dic_curr_parameter:
                if not isinstance(dic_curr_parameter["concomitant"], list):
                    dic_curr_parameter["concomitant"] = [dic_curr_parameter["concomitant"]]
                for concomitant_parameter in dic_curr_parameter["concomitant"]:
                    # Assert that the parameters list have the same size
                    assert len(dic_parameter_lists[parameter]) == len(
                        dic_parameter_lists[concomitant_parameter]
                    ), (
                        f"Parameters {parameter} and {concomitant_parameter} must have the "
                        "same size."
                    )
                # Add to the list for filtering later
                ll_concomitant_parameters.append([parameter] + dic_curr_parameter["concomitant"])

        return (
            dic_parameter_lists,
            dic_parameter_lists_for_naming,
            dic_subvariables,
            ll_concomitant_parameters,
            l_conditions,
        )

    def postprocess_parameter_lists(
        self,
        dic_parameter_lists: dict[str, Any],
        dic_parameter_lists_for_naming: dict[str, Any],
        dic_subvariables: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Post-processes parameter lists by ensuring values are not numpy types and handling nested
        parameters.

        Args:
            dic_parameter_lists (dict[str, Any]): Dictionary containing parameter lists.
            dic_parameter_lists_for_naming (dict[str, Any]): Dictionary containing parameter lists
                for naming.
            dic_subvariables (dict[str, Any]): Dictionary containing subvariables for nested
                parameters.

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: Updated dictionaries of parameter lists and
                parameter lists for naming.
        """
        for parameter, parameter_list in dic_parameter_lists.items():
            parameter_list_for_naming = dic_parameter_lists_for_naming[parameter]

            # Ensure that all values are not numpy types (to avoid serialization issues)
            parameter_list = [x.item() if isinstance(x, np.generic) else x for x in parameter_list]

            # Handle nested parameters
            parameter_list_updated = (
                convert_for_subvariables(dic_subvariables[parameter], parameter_list)
                if parameter in dic_subvariables
                else parameter_list
            )
            # Update the dictionaries
            dic_parameter_lists[parameter] = parameter_list_updated
            dic_parameter_lists_for_naming[parameter] = parameter_list_for_naming

        return dic_parameter_lists, dic_parameter_lists_for_naming

    def create_scans(
        self,
        generation: str,
        generation_path: str,
        template_path: str,
        depth_gen: int,
        dic_parameter_lists: Optional[dict[str, Any]] = None,
        dic_parameter_lists_for_naming: Optional[dict[str, Any]] = None,
        add_prefix_to_folder_names: bool = False,
    ) -> list[str]:
        """
        Creates study files for parametric scans.
        If a dictionary of parameter lists is provided, the scan will be done on the parameter
        lists (no cartesian product). Otherwise, the scan will be done on the cartesian product of
        the parameters defined in the scan configuration file.

        Args:
            generation (str): The generation name.
            generation_path (str): The (relative) path to the generation folder.
            template_path (str): The path to the template folder.
            depth_gen (int): The depth of the generation in the tree.
            dic_parameter_lists (Optional[dict[str, Any]]): The dictionary of parameter lists.
                Defaults to None.
            dic_parameter_lists_for_naming (Optional[dict[str, Any]]): The dictionary of parameter
                lists for naming. Defaults to None.
            add_prefix_to_folder_names (bool): Whether to add a prefix to the folder names. Defaults
                to False.

        Returns:
            tuple[list[str], list[str]]: The list of study file strings and the list of study paths.
        """
        if dic_parameter_lists is None:
            # Get dictionnary of parametric values being scanned
            dic_parameter_lists, dic_parameter_lists_for_naming, array_conditions = (
                self.get_dic_parametric_scans(generation)
            )
            apply_cartesian_product = True
        else:
            if dic_parameter_lists_for_naming is None:
                dic_parameter_lists_for_naming = copy.deepcopy(dic_parameter_lists)
            array_conditions = None
            apply_cartesian_product = False

        # Generate render write for the parameters parameters
        l_study_path = []
        if apply_cartesian_product:
            logging.info(
                f"Now generation cartesian product of all parameters for generation: {generation}"
            )
            array_param_values = itertools.product(*dic_parameter_lists.values())
            array_param_values_for_naming = itertools.product(
                *dic_parameter_lists_for_naming.values()
            )
            array_idx = itertools.product(*[range(len(x)) for x in dic_parameter_lists.values()])
        else:
            logging.info(f"Now generation parameters for generation: {generation}")
            array_param_values = [list(x) for x in zip(*dic_parameter_lists.values())]
            array_param_values_for_naming = [
                list(x) for x in zip(*dic_parameter_lists_for_naming.values())
            ]
            array_idx = range(len(array_param_values))

        # Loop over the parameters
        to_disk_len = np.sum(array_conditions) if array_conditions is not None else 1
        to_disk_idx = 0
        for idx, (l_values, l_values_for_naming, l_idx) in enumerate(
            zip(array_param_values, array_param_values_for_naming, array_idx)
        ):
            # Check the idx to keep if conditions are present
            if array_conditions is not None and not array_conditions[l_idx]:
                continue

            # Create the path for the study
            dic_mutated_parameters = dict(zip(dic_parameter_lists.keys(), l_values))
            dic_mutated_parameters_for_naming = dict(
                zip(dic_parameter_lists.keys(), l_values_for_naming)
            )

            # Handle prefix
            prefix_path = ""
            if add_prefix_to_folder_names:
                prefix_path = f"ID_{str(to_disk_idx).zfill(len(str(to_disk_len)))}_"
                to_disk_idx += 1

            # Handle suffix
            suffix_path = "_".join(
                [
                    f"{parameter}_{value}"
                    for parameter, value in dic_mutated_parameters_for_naming.items()
                ]
            )
            suffix_path = suffix_path.removeprefix("_")

            # Create final path
            path = generation_path + prefix_path + suffix_path + "/"

            # Add common parameters
            if generation in self.dic_common_parameters:
                dic_mutated_parameters |= self.dic_common_parameters[generation]

            # Remove "" from mutated parameters, if it's in the dictionary
            # as it's only used when no scan is done
            if "" in dic_mutated_parameters:
                dic_mutated_parameters.pop("")

            # Generate the study for current generation
            self.generate_render_write(
                generation,
                path,
                template_path,
                depth_gen,
                dic_mutated_parameters=dic_mutated_parameters,
            )

            # Append the list of study paths to build the tree later on
            l_study_path.append(path)

        if not l_study_path:
            logging.warning(
                f"No study paths were created for generation {generation}."
                "Please check the conditions."
            )

        return l_study_path

    def complete_tree(
        self, dictionary_tree: dict, l_study_path_next_gen: list[str], gen: str
    ) -> dict:
        """
        Completes the tree structure of the study dictionary.

        Args:
            dictionary_tree (dict): The dictionary representing the study tree structure.
            l_study_path_next_gen (list[str]): The list of study paths for the next gen.
            gen (str): The generation name.

        Returns:
            dict: The updated dictionary representing the study tree structure.
        """
        logging.info(f"Completing the tree structure for generation: {gen}")
        for path_next in l_study_path_next_gen:
            nested_set(
                dictionary_tree,
                path_next.split("/")[1:-1] + [gen],
                {"file": f"{path_next}{gen}.py"},
            )

        return dictionary_tree

    def write_tree(self, dictionary_tree: dict):
        """
        Writes the study tree structure to a YAML file.

        Args:
            dictionary_tree (dict): The dictionary representing the study tree structure.
        """
        logging.info("Writing the tree structure to a YAML file.")
        ryaml = yaml.YAML()
        with open(self.path_tree, "w") as yaml_file:
            ryaml.indent(sequence=4, offset=2)
            ryaml.dump(dictionary_tree, yaml_file)

    def create_study_for_current_gen(
        self,
        generation: str,
        generation_path: str,
        depth_gen: int,
        dic_parameter_lists: Optional[dict[str, Any]] = None,
        dic_parameter_lists_for_naming: Optional[dict[str, Any]] = None,
        add_prefix_to_folder_names: bool = False,
    ) -> list[str]:
        """
        Creates study files for the current generation.

        Args:
            generation (str): The name of the current generation.
            directory_path (str): The (relative) path to the directory folder for the current
                generation.
            depth_gen (int): The depth of the generation in the tree.
            dic_parameter_lists (Optional[dict[str, Any]]): The dictionary of parameter lists.
                Defaults to None.
            dic_parameter_lists_for_naming (Optional[dict[str, Any]]): The dictionary of parameter
                lists for naming. Defaults to None.
            add_prefix_to_folder_names (bool): Whether to add a prefix to the folder names. Defaults
                to False.

        Returns:
            tuple[list[str], list[str]]: The list of study file strings and the list of study paths.
        """
        executable_path = self.config["structure"][generation]["executable"]
        path_local_template = (
            f"{os.path.dirname(inspect.getfile(GenerateScan))}/../assets/template_scripts/"
        )

        # Check if the executable path corresponds to a file
        if not os.path.isfile(executable_path):
            # Check if the executable path corresponds to a file in the template folder
            executable_path_template = f"{path_local_template}{executable_path}"
            if not os.path.isfile(executable_path_template):
                raise FileNotFoundError(
                    f"Executable file {executable_path} not found locally nor in the study-da "
                    "template folder."
                )
            else:
                executable_path = executable_path_template

        # Ensure that the values in dic_parameter_lists can be dumped with ryaml
        if dic_parameter_lists is not None:
            # Recursively convert all numpy types to standard types
            clean_dic(dic_parameter_lists)
            logging.info("An external dictionary of parameters was provided.")
        else:
            logging.info("Creating the dictionnary of parameters from the configuration file.")

        return self.create_scans(
            generation,
            generation_path,
            executable_path,
            depth_gen,
            dic_parameter_lists,
            dic_parameter_lists_for_naming,
            add_prefix_to_folder_names,
        )

    def browse_and_creat_study(
        self,
        dic_parameter_all_gen: Optional[dict[str, dict[str, Any]]],
        dic_parameter_all_gen_naming: Optional[dict[str, dict[str, Any]]],
        add_prefix_to_folder_names: bool,
    ) -> dict:
        l_study_path = [self.config["name"] + "/"]
        dictionary_tree = {}

        # Browse through the generations
        l_generations = list(self.config["structure"].keys())
        for idx, generation in enumerate(l_generations):
            l_study_path_all_next_generation = []
            logging.info(f"Taking care of generation: {generation}")
            for study_path in l_study_path:
                if dic_parameter_all_gen is None or generation not in dic_parameter_all_gen:
                    dic_parameter_current_gen = None
                    dic_parameter_naming_current_gen = None
                else:
                    dic_parameter_current_gen = dic_parameter_all_gen[generation]
                    if (
                        dic_parameter_all_gen_naming is not None
                        and generation in dic_parameter_all_gen_naming
                    ):
                        dic_parameter_naming_current_gen = dic_parameter_all_gen_naming[generation]
                    else:
                        dic_parameter_naming_current_gen = None

                # Get list of paths for the children of the current study
                l_study_path_next_generation = self.create_study_for_current_gen(
                    generation,
                    study_path,
                    idx + 1,
                    dic_parameter_current_gen,
                    dic_parameter_naming_current_gen,
                    add_prefix_to_folder_names,
                )
                # Update tree
                dictionary_tree = self.complete_tree(
                    dictionary_tree, l_study_path_next_generation, generation
                )
                # Complete list of paths for the children of all studies (of the current generation)
                l_study_path_all_next_generation.extend(l_study_path_next_generation)

            # Update study path for next later
            l_study_path = l_study_path_all_next_generation

        return dictionary_tree

    def create_study(
        self,
        tree_file: bool = True,
        force_overwrite: bool = False,
        dic_parameter_all_gen: Optional[dict[str, dict[str, Any]]] = None,
        dic_parameter_all_gen_naming: Optional[dict[str, dict[str, Any]]] = None,
        add_prefix_to_folder_names: bool = False,
    ) -> None:
        """
        Creates study files for the entire study.

        Args:
            tree_file (bool, optional): Whether to write the study tree structure to a YAML file.
                Defaults to True.
            force_overwrite (bool, optional): Whether to overwrite existing study files.
                Defaults to False.
            dic_parameter_all_gen (Optional[dict[str, dict[str, Any]]]): The dictionary of parameter
                lists for all generations. Defaults to None.
            dic_parameter_all_gen_naming (Optional[dict[str, dict[str, Any]]]): The dictionary of
                parameter lists for all generations for naming. Defaults to None.
            add_prefix_to_folder_names (bool): Whether to add a prefix to the folder names. Defaults
                to False.

        Returns:
            list[str]: The list of study file strings.
        """

        # Raise an error if dic_parameter_all_gen_naming is not None while dic_parameter_all_gen is None
        if dic_parameter_all_gen is None and dic_parameter_all_gen_naming is not None:
            raise ValueError(
                "If dic_parameter_all_gen_naming is defined, dic_parameter_all_gen must be defined."
            )

        # Remove existing study if force_overwrite
        if os.path.exists(self.config["name"]):
            if not force_overwrite:
                logging.info(
                    f"Study {self.config['name']} already exists. Set force_overwrite to True to "
                    "overwrite. Continuing without overwriting."
                )
                return
            shutil.rmtree(self.config["name"])

        # Browse through the generations and create the study
        dictionary_tree = self.browse_and_creat_study(
            dic_parameter_all_gen,
            dic_parameter_all_gen_naming,
            add_prefix_to_folder_names,
        )

        # Add dependencies to root of the study
        if "dependencies" in self.config:
            for dependency, path in self.config["dependencies"].items():
                # Check if the dependency exists as a file
                if not os.path.isfile(path):
                    # Check if the dependency exists as a file in the template folder
                    path_template = f"{os.path.dirname(inspect.getfile(GenerateScan))}/../assets/configurations/{path}"
                    if not os.path.isfile(path_template):
                        raise FileNotFoundError(
                            f"Dependency file {path} not found locally nor in the study-da "
                            "template folder."
                        )
                    else:
                        path = path_template
                shutil.copy2(path, self.config["name"])

        if tree_file:
            self.write_tree(dictionary_tree)

    @staticmethod
    def eval_conditions(l_condition: list[str], dic_parameter_lists: dict[str, Any]) -> np.ndarray:
        """
        Evaluates the conditions to filter out some parameter values.

        Args:
            l_condition (list[str]): The list of conditions.
            dic_parameter_lists (dict[str: Any]): The dictionary of parameter lists.

        Returns:
            np.ndarray: The array of conditions.
        """
        # Initialize the array of parameters as a meshgrid of all parameters
        l_parameters = list(dic_parameter_lists.values())
        meshgrid = np.meshgrid(*l_parameters, indexing="ij")

        # Associate the parameters to their names
        dic_param_mesh = dict(zip(dic_parameter_lists.keys(), meshgrid))

        # Evaluate the conditions and take the intersection of all conditions
        array_conditions = np.ones_like(meshgrid[0], dtype=bool)
        for condition in l_condition:
            array_conditions = array_conditions & eval(condition, dic_param_mesh)

        return array_conditions

    @staticmethod
    def filter_for_concomitant_parameters(
        array_conditions: np.ndarray,
        ll_concomitant_parameters: list[list[str]],
        dic_dimension_indices: dict[str, int],
    ) -> np.ndarray:
        """
        Filters the conditions for concomitant parameters.

        Args:
            array_conditions (np.ndarray): The array of conditions.
            ll_concomitant_parameters (list[list[str]]): The list of concomitant parameters.
            dic_dimension_indices (dict[str, int]): The dictionary of dimension indices.

        Returns:
            np.ndarray: The filtered array of conditions.
        """

        # Return the array of conditions if no concomitant parameters
        if not ll_concomitant_parameters:
            return array_conditions

        # Get the indices of the concomitant parameters
        ll_idx_concomitant_parameters = [
            [dic_dimension_indices[parameter] for parameter in concomitant_parameters]
            for concomitant_parameters in ll_concomitant_parameters
        ]

        # Browse all the values of array_conditions
        for idx, _ in np.ndenumerate(array_conditions):
            # Check if the value is on the diagonal of the concomitant parameters
            for l_idx_concomitant_parameter in ll_idx_concomitant_parameters:
                if any(
                    idx[i] != idx[j]
                    for i, j in itertools.combinations(l_idx_concomitant_parameter, 2)
                ):
                    array_conditions[idx] = False
                    break

        return array_conditions
