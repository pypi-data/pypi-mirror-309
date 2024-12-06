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
from pyspark.sql.types import BinaryType
from pyspark.sql.types import StringType




class CustomDataSchemaBase(ABC):
    """
    Base implementation of the PySpark schema for CustomData.

    GENERATED CODE - DO NOT MODIFY (add your customizations in CustomData).

    Generated from: templates/data-delivery-data-records/pyspark.schema.base.py.vm
    """

    CUSTOM_FIELD_COLUMN: str = 'customField'
    BINARY_FIELD_COLUMN: str = 'binaryField'


    def __init__(self):
        self._schema = StructType()

        self.add(CustomDataSchemaBase.CUSTOM_FIELD_COLUMN, StringType(), True)
        self.add(CustomDataSchemaBase.BINARY_FIELD_COLUMN, BinaryType(), True)


    def cast(self, dataset: DataFrame) -> DataFrame:
        """
        Returns the given dataset cast to this schema.
        """
        custom_field_type = self.get_data_type(CustomDataSchemaBase.CUSTOM_FIELD_COLUMN)
        binary_field_type = self.get_data_type(CustomDataSchemaBase.BINARY_FIELD_COLUMN)

        return dataset \
            .withColumn(CustomDataSchemaBase.CUSTOM_FIELD_COLUMN, dataset[CustomDataSchemaBase.CUSTOM_FIELD_COLUMN].cast(custom_field_type)) \
            .withColumn(CustomDataSchemaBase.BINARY_FIELD_COLUMN, dataset[CustomDataSchemaBase.BINARY_FIELD_COLUMN].cast(binary_field_type))


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
