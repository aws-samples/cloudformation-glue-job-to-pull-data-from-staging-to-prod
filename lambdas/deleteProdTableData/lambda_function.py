# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import pymysql, boto3


def lambda_handler(event, context):
    ssm = boto3.client("ssm")

    table_name = event["TableName"]
    database = ssm.get_parameter(
        Name="mysql-staging-db-name", WithDecryption=True
    )["Parameter"]["Value"]
    host = ssm.get_parameter(Name="mysql-endpoint", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    port = int(
        ssm.get_parameter(Name="mysql-port", WithDecryption=True)["Parameter"][
            "Value"
        ]
    )
    user = ssm.get_parameter(Name="mysql-username", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    password = ssm.get_parameter(Name="mysql-password", WithDecryption=True)[
        "Parameter"
    ]["Value"]

    query = f"""TRUNCATE TABLE `aws`.{table_name};"""
    conn = pymysql.connect(
        database=database, host=host, port=port, user=user, password=password
    )

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    conn.close()

    return {
        "statusCode": 200,
    }
