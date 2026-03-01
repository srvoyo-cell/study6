import sys
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix, save_npz, load_npz
from task3 import X_base


data = [1, 2, 3, 4, 5]
rows = [0, 1, 2, 0, 1]
cols = [0, 2, 1, 3, 4]

coo = coo_matrix((data, (rows, cols)), shape=(3, 5))
print("COO формат:")
print(f" Данные: {coo.data}")
print(f" Строки: {coo.row}")
print(f" Столбцы: {coo.col}")
print(f" Матрица:\n{coo.toarray()}")

csr = coo.tocsr()
print("CSR формат:")
print(f" Данные: {csr.data}")
print(f" Индексы столбцов: {csr.indices}")
print(f" Указатели строк: {csr.indptr}")

csc = coo.tocsc()
print("CSC формат:")
print(f" Данные: {csc.data}")
print(f" Индексы строк: {csc.indices}")
print(f" Указатели столбцов: {csc.indptr}")


def get_size(obj):
    return sys.getsizeof(obj)


dense_matrix = X_base.toarray()
dense_size = get_size(dense_matrix) + dense_matrix.nbytes

coo_matrix_sp = coo_matrix(X_base)
csr_matrix_sp = csr_matrix(X_base)
csc_matrix_sp = csc_matrix(X_base)

print(f"Плотная матрица: {dense_size / 1024:.2f} KB")
print(f"COO формат: {get_size(coo_matrix_sp) / 1024:.2f} KB")
print(f"CSR формат: {get_size(csr_matrix_sp) / 1024:.2f} KB")
print(f"CSC формат: {get_size(csc_matrix_sp) / 1024:.2f} KB")
print(f"Экономия памяти (CSR vs плотная): {(1 - get_size(csr_matrix_sp) / dense_size) * 100:.2f}%")

save_npz("sparse_matrix.npz", X_base)
X_loaded = load_npz("sparse_matrix.npz")
print(f"Загруженная матрица: размер {X_loaded.shape}, ненулевых {X_loaded.nnz}")
print(f"Матрицы идентичны: {(X_base != X_loaded).nnz == 0}")
