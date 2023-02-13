import erppeek

# class local():
#     SERVER = "http://localhost:8069/"
#     DATABASE = "dev"
#     USERNAME = "admin"
#     PASSWORD = "123"
#     client = erppeek.Client(
#         SERVER,
#         DATABASE,
#         USERNAME,
#         PASSWORD
#     )
#     def get_client(self):
#         return self.client

# class dev():
#     SERVER = "https://dev.saleholding.com/"
#     DATABASE = "dev"
#     USERNAME = "admin"
#     PASSWORD = "Hebela@123"
#     client = erppeek.Client(
#         SERVER,
#         DATABASE,
#         USERNAME,
#         PASSWORD
#     )
#     def get_client(self):
#         return self.client

class stage():
    SERVER = "https://stage.saleholding.com/"
    DATABASE = "saleholding2"
    USERNAME = "tuan.bui3@hebela.net"
    PASSWORD = "Admin@123"
    client = erppeek.Client(
        SERVER,
        DATABASE,
        USERNAME,
        PASSWORD
    )
    def get_client(self):
        return self.client

# class product():
#     SERVER = "https://saleholding.com/"
#     DATABASE = "saleholding"
#     USERNAME = "tuan.bui3@hebela.net"
#     PASSWORD = "Admin@123"
#     client = erppeek.Client(
#         SERVER,
#         DATABASE,
#         USERNAME,
#         PASSWORD
#     )
#     def get_client(self):
#         return self.client
