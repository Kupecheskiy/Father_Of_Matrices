import numpy as np


class Matrix:
    # Класс, представляющий матрицу.
    
    def __init__(self, data):
        # Создаёт матрицу из списка списков или numpy-массива.
        if isinstance(data, np.ndarray):
            self.data = data
        else:
            self.data = np.array(data)
    
    @classmethod
    def from_text(cls, text: str):
        # Создаёт матрицу из текстового ввода пользователя.
        rows = text.strip().split("\n")
        rows = [row.strip() for row in rows if row.strip()]
        if not rows:
            raise ValueError("Вы не ввели ни одной строки.")
        
        matrix_data = []
        for i, row in enumerate(rows, 1):
            row = row.replace(",", " ").replace(";", " ")
            parts = row.split()
            if not parts:
                raise ValueError(f"Строка {i} пуста.")
            try:
                nums = list(map(float, parts))
            except ValueError:
                raise ValueError(f"Строка {i} содержит нечисловое значение: '{row}'")
            matrix_data.append(nums)
        
        lengths = [len(r) for r in matrix_data]
        if len(set(lengths)) != 1:
            raise ValueError(f"Строки имеют разную длину: {lengths}")
        
        return cls(matrix_data)
    
    def _format_number(self, x: float) -> str:
        # Форматирует одно число.
        if abs(x - round(x)) < 1e-10:
            return str(int(round(x)))
        s = f"{x:.4f}".rstrip('0').rstrip('.')
        return s
    
    def __str__(self):
        # Красивый вывод матрицы.
        return "\n".join(" ".join(self._format_number(num) for num in row) for row in self.data)
    
    def __add__(self, other):
        # Сложение матриц.
        if self.data.shape != other.data.shape:
            raise ValueError("Для сложения размеры матриц должны совпадать.")
        return Matrix(self.data + other.data)
    
    def __sub__(self, other):
        # Вычитание матриц.
        if self.data.shape != other.data.shape:
            raise ValueError("Для вычитания размеры матриц должны совпадать.")
        return Matrix(self.data - other.data)
    
    def __matmul__(self, other):
        # Умножение матриц.
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Количество столбцов первой матрицы должно быть равно количеству строк второй.")
        return Matrix(self.data @ other.data)
    
    def transpose(self):
        # Транспонирование.
        return Matrix(self.data.T)
    
    def determinant(self):
        # Определитель.
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError("Определитель можно найти только у квадратной матрицы.")
        try:
            return np.linalg.det(self.data)
        except np.linalg.LinAlgError:
            raise ValueError("Не удалось вычислить определитель.")
    
    def inverse(self):
        # Обратная матрица.
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError("Обратную матрицу можно найти только у квадратной матрицы.")
        try:
            return Matrix(np.linalg.inv(self.data))
        except np.linalg.LinAlgError:
            raise ValueError("Матрица вырождена. Обратной матрицы не существует.")
    
    def rank(self):
        # Ранг матрицы.
        return np.linalg.matrix_rank(self.data)
    
    @property
    def shape(self):
        # Размер матрицы.
        return self.data.shape