from points_decorator import points
import inspect
import pandas as pd
import geopandas as gpd
import pyproj



class TestProblem3:
    @points(2, "Problem 3, Part 1: Did you import the population grid`?")
    def test_problem_3_part_1_grid(self, problem3):
        section_data, namespace = problem3
        section = "Part 1"
        variables = section_data[section]['variables']
        source = section_data[section]['source']

        assert isinstance(variables['population_grid'], pd.DataFrame)
        assert 'asukkaita' or 'population' in variables['population_grid'].columns
        assert "wfs" in source

    @points(2, "Problem 3, Part 1: Did you import the shopping centre buffers?")
    def test_problem_3_part_1_centres(self, problem3):
        section_data, namespace = problem3
        section = "Part 1"
        variables = section_data[section]['variables']

        assert isinstance(variables['shopping_centre_buffers'], pd.DataFrame)
        assert len(variables['shopping_centre_buffers']) == 7

    
    @points(2, "Problem 3, Part 2: Did you import the shopping centre buffers into a dataframe?")
    def test_problem_3_part_2(self, problem3):
        section_data, namespace = problem3
        section = "Part 2"
        variables = section_data[section]['variables']
        source = section_data[section]['source']

        assert "sjoin" in source
        assert "within" in source


    @points(2, "Problem 3, Part 3: Are the population numbers for the shopping centres realistic?")
    def test_problem_3_part_3_population(self, problem3):
        section_data, namespace = problem3
        section = "Part 3"
        variables = section_data[section]['variables']
        source = section_data[section]['source']

        shopping_centre_grouped = variables['shopping_centre_grouped']

        # Expected population values for each shopping centre
        expected_population = {
            "Forum": 55504,
            "Iso Omena": 26698,
            "Itis": 20889,
            "Jumbo": 10956,
            "REDI": 26341,
            "Sello": 24877,
            "Tripla": 24394,
        }

        # Tolerance for the population values
        tolerance = 1000

        # Assert that the population values are within the tolerance
        for name, expected_value in expected_population.items():
            actual_value = shopping_centre_grouped[name]
            assert abs(actual_value - expected_value) <= tolerance
                
