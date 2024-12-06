###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.column import Column
from pyspark.sql.types import StructType
from pyspark.sql.types import DataType
from pyspark.sql.functions import col
from typing import List
import types
from pyspark.sql.types import StringType




class RecordWithPoliciesSchemaBase(ABC):
    """
    Base implementation of the PySpark schema for RecordWithPolicies.

    GENERATED CODE - DO NOT MODIFY (add your customizations in RecordWithPolicies).

    Generated from: templates/data-delivery-data-records/pyspark.schema.base.py.vm
    """

    FIELD_WITH_POLICIES_COLUMN: str = 'fieldWithPolicies'
    FIELD_WITH_DICTIONARY_TYPE_POLICIES_COLUMN: str = 'fieldWithDictionaryTypePolicies'
    FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN_COLUMN: str = 'fieldWithDictionaryTypePoliciesOverridden'


    def __init__(self):
        self._schema = StructType()

        self.add(RecordWithPoliciesSchemaBase.FIELD_WITH_POLICIES_COLUMN, StringType(), True)
        self.add(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_COLUMN, StringType(), True)
        self.add(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN_COLUMN, StringType(), True)


    def cast(self, dataset: DataFrame) -> DataFrame:
        """
        Returns the given dataset cast to this schema.
        """
        field_with_policies_type = self.get_data_type(RecordWithPoliciesSchemaBase.FIELD_WITH_POLICIES_COLUMN)
        field_with_dictionary_type_policies_type = self.get_data_type(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_COLUMN)
        field_with_dictionary_type_policies_overridden_type = self.get_data_type(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN_COLUMN)

        return dataset \
            .withColumn(RecordWithPoliciesSchemaBase.FIELD_WITH_POLICIES_COLUMN, dataset[RecordWithPoliciesSchemaBase.FIELD_WITH_POLICIES_COLUMN].cast(field_with_policies_type)) \
            .withColumn(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_COLUMN, dataset[RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_COLUMN].cast(field_with_dictionary_type_policies_type)) \
            .withColumn(RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN_COLUMN, dataset[RecordWithPoliciesSchemaBase.FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN_COLUMN].cast(field_with_dictionary_type_policies_overridden_type))


    @property
    def struct_type(self) -> StructType:
        """
        Returns the structure type for this schema.
        """
        return self._schema


    @struct_type.setter
    def struct_type(self, struct_type: StructType) -> None:
        raise Exception('Schema structure type should not be set manually!')


    def get_data_type(self, name: str) -> str:
        """
        Returns the data type for a field in this schema.
        """
        data_type = None
        if name in self._schema.fieldNames():
            data_type = self._schema[name].dataType

        return data_type


    def add(self, name: str, data_type: DataType, nullable: bool) -> None:
        """
        Adds a field to this schema.
        """
        self._schema.add(name, data_type, nullable)


    def update(self, name: str, data_type: DataType) -> None:
        """
        Updates the data type of a field in this schema.
        """
        fields = self._schema.fields
        if fields and len(fields) > 0:
            update = StructType()
            for field in fields:
                if field.name == name:
                    update.add(name, data_type, field.nullable)
                else:
                    update.add(field)

            self._schema = update

    def validate_dataset(self, ingest_dataset: DataFrame) -> DataFrame:
        """
        Validates the given dataset and returns the lists of validated records.
        """
        data_with_validations = ingest_dataset

        validation_columns = [x for x in data_with_validations.columns if x not in ingest_dataset.columns]

        # Schema for filtering for valid data
        filter_schema = None
        for column_name in validation_columns:
            if isinstance(filter_schema, Column):
                filter_schema = filter_schema & col(column_name).eqNullSafe(True)
            else:
                filter_schema = col(column_name).eqNullSafe(True)

        valid_data = data_with_validations
        # Isolate the valid data and drop validation columns
        if isinstance(filter_schema, Column):
            valid_data = data_with_validations.filter(filter_schema)
        valid_data = valid_data.drop(*validation_columns)
        return valid_data
