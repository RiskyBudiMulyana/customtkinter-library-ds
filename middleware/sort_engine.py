class SortEngine:
    @staticmethod
    def bubble_sort(data_list, key='title'):
        """Bubble Sort -> O(n^2) Family: Algoritma penukaran dasar untuk abjad judul."""
        n = len(data_list)
        arr = list(data_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j][key].lower() > arr[j + 1][key].lower():
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def quick_sort(data_list):
        """Quick Sort -> O(n log n) Family: Divide & conquer efisiensi tinggi skala besar (ID Buku)."""
        if len(data_list) <= 1:
            return data_list
        pivot = data_list[len(data_list) // 2]['id']
        left = [x for x in data_list if x['id'] < pivot]
        middle = [x for x in data_list if x['id'] == pivot]
        right = [x for x in data_list if x['id'] > pivot]
        return SortEngine.quick_sort(left) + middle + SortEngine.quick_sort(right)