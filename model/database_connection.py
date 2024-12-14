import firebase_admin
import google
from firebase_admin import credentials, firestore


class DatabaseConnection:
    _cred = None
    _connection = None

    def __new__(cls):
        # Kiểm tra xem instance đã tồn tại chưa
        if cls._cred is None:
            # Nếu chưa, tạo một instance mới và thiết lập kết nối
            cls._cred = credentials.Certificate("/etc/secrets/credentials.json")

            # Khởi tạo Firebase
            firebase_admin.initialize_app(cls._cred)
            try:
                cls._connection = firestore.client()
                print("Database connection established!")
            except ValueError as e:
                print(f"Error: {e}")
                cls._connection = None
        return cls

    @staticmethod
    def get_connection() -> google.cloud.firestore_v1.client.Client:
        # Trả về kết nối cơ sở dữ liệu
        if DatabaseConnection._connection:
            return DatabaseConnection._connection
        else:
            raise Exception("Database connection failed!")


if __name__ == '__main__':
    db = DatabaseConnection()
    try:
        ref = db.get_connection().collection('shop')
        docs = ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
    except Exception as e:
        print(e)