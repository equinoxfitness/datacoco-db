import boto3
from botocore.exceptions import ClientError
import awswrangler as wr
from botocore.config import Config


NULL_VALS = ("None", "")


class DynamoInteraction:

    # pylint: disable=too-many-locals
    def __init__(
        self,
        table_name,
        aws_access_key_id,
        aws_secret_access_key,
        create=True,
        pk=None,
        sk=None,
        billing_mode=None,
        rcu=None,
        wcu=None,
        gsi=None,
    ):
        config = Config(
            read_timeout=900,
            connect_timeout=900,
            retries={"max_attempts": 0}
        )
        self._session = sess = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name='us-east-1'
        )
        self.dynamo = sess.resource('dynamodb')
        self.client = sess.client('dynamodb', config=config)
        self.table = self.dynamo.Table(table_name)

        self.table_name = table_name

        if create:
            try:
                self.client.describe_table(TableName=table_name)
            except ClientError:
                if sk:
                    keys = pk + "," + sk
                    pk_str = f'{pk.split("-")[0]}-HASH'
                    sk_str = f'{sk.split("-")[0]}-RANGE'
                    schema = f'{pk_str},{sk_str}'
                else:  # only pk
                    keys = pk
                    schema = pk.split("-")[0] + "-HASH"
                print(f"""
                    Dynamo table {table_name} did not exist, creating table...
                """)
                self.create_table(
                    keys=keys,
                    schema=schema,
                    billing_mode=billing_mode,
                    rcu=rcu,
                    wcu=wcu,
                    gsi=gsi,
                )
        else:
            print("create was false, did not try to create table")

    # pylint: disable=too-many-locals
    def create_table(self,
                     keys,
                     schema,
                     billing_mode,
                     rcu=None,
                     wcu=None,
                     gsi=None
                     ):
        # keys = 'pk-S,sk-B'
        # key_schema = 'pk-HASH,sk-RANGE'
        # billing_mode = PROVISIONED | PAY_PER_REQUEST
        attribute_definitions = []

        for key in keys.split(","):
            k, t = key.split("-")
            attr_dict = {"AttributeName": k, "AttributeType": t}
            attribute_definitions.append(attr_dict)

        if gsi:
            gsi_attr_dict_data = gsi.split("|")[0]
            gsi_attr_dict = {
                    "AttributeName": gsi_attr_dict_data,
                    "AttributeType": "S"
            }
            attribute_definitions.append(gsi_attr_dict)

        key_schema = []

        for scheme in schema.split(","):
            k, t = scheme.split("-")
            schema_dict = {"AttributeName": k, "KeyType": t}
            key_schema.append(schema_dict)

        if billing_mode == "PROVISIONED":
            provisioned_throughput = {
                "ReadCapacityUnits": rcu,
                "WriteCapacityUnits": wcu,
            }

            if gsi:

                gsis = []

                # pylint: disable=line-too-long
                index_name, schema, projection, gsi_rcu, gsi_wcu = gsi.split("|")

                gsi_key_schema = []
                k, t = schema.split("@")
                gsi_key_schema_dict = {"AttributeName": k, "KeyType": t}
                gsi_key_schema.append(gsi_key_schema_dict)

                gsi_provisioned_throughput = {
                    "ReadCapacityUnits": int(gsi_rcu),
                    "WriteCapacityUnits": int(gsi_wcu),
                }

                gsi_dict = {
                    "IndexName": f"{index_name}-index",
                    "KeySchema": gsi_key_schema,
                    "Projection": {"ProjectionType": projection},
                    "ProvisionedThroughput": gsi_provisioned_throughput,
                }

                gsis.append(gsi_dict)

                self.client.create_table(
                    AttributeDefinitions=attribute_definitions,
                    TableName=self.table_name,
                    KeySchema=key_schema,
                    BillingMode=billing_mode,
                    GlobalSecondaryIndexes=gsis,
                    ProvisionedThroughput=provisioned_throughput,
                )

            else:

                self.client.create_table(
                    AttributeDefinitions=attribute_definitions,
                    TableName=self.table_name,
                    KeySchema=key_schema,
                    BillingMode=billing_mode,
                    ProvisionedThroughput=provisioned_throughput,
                )

        else:  # on demand capacity
            self.client.create_table(
                AttributeDefinitions=attribute_definitions,
                TableName=self.table_name,
                KeySchema=key_schema,
                BillingMode=billing_mode,
            )

            self.exists_waiter(poll=5, max_attempts=25)

    def exists_waiter(self, poll=20, max_attempts=25):
        waiter = self.client.get_waiter("table_exists")
        waiter_config = {"Delay": poll, "MaxAttempts": max_attempts}
        waiter.wait(TableName=self.table_name, WaiterConfig=waiter_config)
        print(f"Table {self.table_name} exists in active state!")

    def write_df_to_dynamo(self, df):
        """write to from df to dynamo """
        with self.table.batch_writer() as batch:
            for records in df:
                dict_records = records.astype(str).to_dict("records")
                for i, record in enumerate(dict_records):
                    if i % 1000 == 0:
                        print(f"Writing record {i}")
                    item = {
                        k: v for k, v in record.items()
                        if v not in NULL_VALS
                    }
                    try:
                        batch.put_item(Item=item)
                    except ClientError:
                        print(item)
                        raise

    def write_records_to_dynamo(self, records):
        """write to from df to dynamo """
        with self.table.batch_writer() as batch:
            for i, record in enumerate(records.astype(str).to_dict("records")):
                item = {k: v for k, v in record.items() if v not in NULL_VALS}
                if i % 1000 == 0:
                    print(f"Writing record {i}")
                try:
                    batch.put_item(Item=item)
                except ClientError:
                    print(item)
                    raise

    def delete_table(self, table):
        try:
            self.client.delete_table(TableName=table)
            self.not_exists_waiter(table, poll=5, max_attempts=25)
            print(f"Dynamo Table {table} deleted")
        except ClientError:
            print(f"Dynamo Table {table} did not exist!")

    def not_exists_waiter(self, table, poll=20, max_attempts=25):
        waiter = self.client.get_waiter("table_not_exists")
        waiter_config = {"Delay": poll, "MaxAttempts": max_attempts}
        waiter.wait(TableName=table, WaiterConfig=waiter_config)
        print(f"Table {table} exists in active state!")

    def clear(self, key):
        scan = self.table.scan()
        with self.table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key={
                        key: each[key]
                    }
                )

    def s3_to_dynamo(self,
                     s3_path,
                     partition_key,
                     use_threads=False,
                     chunked=100_000
                     ):
        print(f's3_to_dynamo: {partition_key}')
        if partition_key:
            df = wr.s3.read_parquet(
                path=s3_path,
                boto3_session=self._session,
                use_threads=use_threads,
                chunked=chunked
            )
            self.write_df_to_dynamo(df)
        else:
            records = wr.s3.read_parquet(
                path=s3_path,
                boto3_session=self._session,
                use_threads=use_threads
            )
            self.write_records_to_dynamo(records)

        print('done s3_to_dynamo')
