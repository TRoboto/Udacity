import unittest
import pandas as pd
import numpy as np
import tensorflow as tf
from student_utils import *
from utils import *

class ProjectTesting(unittest.TestCase):

    # first_encounter_df = select_first_encounter(reduce_dim_df)
    def test_reduce_dimension_ndc(self):
        dataset_path = "./data/final_project_dataset.csv"
        df = pd.read_csv(dataset_path)
        ndc_code_path = "./medication_lookup_tables/final_ndc_lookup_table"
        ndc_code_df = pd.read_csv(ndc_code_path)
        reduce_dim_df = reduce_dimension_ndc(df, ndc_code_df)
        unique_ndc_vals = df['ndc_code'].nunique()
        unique_generic_vals = reduce_dim_df['generic_drug_name'].nunique()
        self.assertTrue(unique_ndc_vals > unique_generic_vals )

    def test_select_first_encounter(self):
        reduce_dim_path = "./testing_data/reduce_dim_df.csv"
        reduce_dim_df = pd.read_csv(reduce_dim_path)
        first_encounter_df = select_first_encounter(reduce_dim_df)
        unique_patients = first_encounter_df['patient_nbr'].nunique()
        print("Number of unique patients:{}".format(unique_patients))
        # unique encounters in transformed dataset
        unique_encounters = first_encounter_df['encounter_id'].nunique()
        print("Number of unique encounters:{}".format(unique_encounters))
        original_unique_patient_number = reduce_dim_df['patient_nbr'].nunique()
        # number of unique patients should be equal to the number of unique encounters and patients in the final dataset
        self.assertEqual(original_unique_patient_number, unique_patients)
        self.assertEqual(original_unique_patient_number, unique_encounters)
        print("Tests passed!!")

    def test_patient_dataset_splitter(self):
        processed_df = pd.read_csv("./testing_data/processed_df.csv")
        d_train, d_val, d_test = patient_dataset_splitter(processed_df, 'patient_nbr')
        split_len =len(d_train) + len(d_val) + len(d_test)
        processed_len = len(processed_df)
        self.assertEqual(split_len, processed_len)
        print("Test passed for number of total rows equal!")
        split_unique_patients = (d_train['patient_nbr'].nunique() + d_val['patient_nbr'].nunique() + d_test['patient_nbr'].nunique())
        df = pd.read_csv('./data/final_project_dataset.csv')
        original_unique_patients =  df['patient_nbr'].nunique()
        self.assertEqual(split_unique_patients, original_unique_patients)
        print("Test passed for number of unique patients being equal!")

    def test_create_tf_categorical_feature_cols(self):
        student_categorical_col_list = ['race', 'gender', 'age' ]
        df = pd.read_csv('./data/final_project_dataset.csv')
        batch_size = 128
        PREDICTOR ='time_in_hospital'
        diabetes_train_ds = df_to_dataset(df[ student_categorical_col_list + [PREDICTOR] ], PREDICTOR, batch_size=batch_size)
        diabetes_batch = next(iter(diabetes_train_ds))[0]
        tf_cat_col_list = create_tf_categorical_feature_cols(student_categorical_col_list)
        test_cat_var1 = tf_cat_col_list[0]
        print("Example categorical field:\n{}".format(test_cat_var1))
        self.assertIsNotNone(demo(test_cat_var1, diabetes_batch) )

    def test_create_tf_numerical_feature_cols(self):
        student_numerical_col_list = ['num_lab_procedures', 'num_medications', 'number_diagnoses']
        df = pd.read_csv('./data/final_project_dataset.csv')
        batch_size = 128
        PREDICTOR ='time_in_hospital'
        diabetes_train_ds = df_to_dataset(df[ student_numerical_col_list + [PREDICTOR] ], PREDICTOR, batch_size=batch_size)
        diabetes_batch = next(iter(diabetes_train_ds))[0]
        tf_cont_col_list = create_tf_numerical_feature_cols(student_numerical_col_list, df[student_numerical_col_list])
        test_cont_var1 = tf_cont_col_list[0]
        print("Example continuous field:\n{}\n".format(test_cont_var1))
        self.assertIsNotNone(demo(test_cont_var1, diabetes_batch) )

    def test_student_binary_prediction(self):
        prob_output_df = pd.read_csv("./testing_data/prob_output_df.csv")
        student_binary_prediction = get_student_binary_prediction(prob_output_df, 'pred_mean')
        self.assertListEqual([0,1], list(np.unique(student_binary_prediction)))

if __name__ == '__main__':
    unittest.main()
