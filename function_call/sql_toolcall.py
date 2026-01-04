# from google.genai import types
# def get_sql():
#     # get_sql={
#     #     "name":"get_sql",
#     #     "description": "Generate an SQL query to retrieve the answer from the database.",
#     #     "parameters":{
#     #         "type":"object",
#     #         "parameteres":{
#     #             "question":{
#     #                 "type":"string",
#     #                 "description":"the question asked by the user regarding the database"
#     #             }
#     #         },
#     #         "required":["question","schema_info"]
#     #     }
        
#     # }
#     # return get_sql
#     return types.FunctionDeclaration(
#         name="run",
#         description="Generate an SQL query, retrieve the information, and generate a summary from the information based on the question given.",
#         parameters=types.Schema(
#             type=types.SchemaType.OBJECT,
#             properties={
#                 "question": types.Schema(
#                     type=types.SchemaType.STRING,
#                     description="the question asked by the user regarding the information stored within the database."
#                 )
#             },
#             required=["question"]
#         )
#     )  