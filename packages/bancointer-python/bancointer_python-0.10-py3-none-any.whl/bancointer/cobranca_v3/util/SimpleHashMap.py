class SimpleHashMap:
    def __init__(self, size=100):
        self.size = size
        self.buckets = [
            [] for _ in range(size)
        ]  # Lista de buckets para lidar com colisões

    def hash_function(self, key):
        return sum(ord(char) for char in key) % self.size  # Função hash simples

    def put(self, key, value):
        index = self.hash_function(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Atualiza o valor se a chave já existir
                return
        bucket.append((key, value))  # Adiciona novo par chave-valor

    def get(self, key):
        index = self.hash_function(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v  # Retorna o valor associado à chave
        return None  # Chave não encontrada

    def remove(self, key):
        index = self.hash_function(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]  # Remove o par chave-valor
                return


#
# # Uso do SimpleHashMap
# hash_map = SimpleHashMap()
# hash_map.put("nome", "Alice")
# print(hash_map.get("nome"))  # Saída: Alice
# hash_map.remove("nome")
# print(hash_map.get("nome"))  # Saída: None
