class SearchEngine:
    @staticmethod
    def linear_search(data_list, target_title):
        """Linear Search -> O(n): Pemindaian sekuensial berdasarkan kecocokan judul."""
        results = []
        for index, item in enumerate(data_list):
            if target_title.lower() in item['title'].lower():
                results.append((index, item))
        return results

    @staticmethod
    def binary_search(sorted_list, target_id):
        """Binary Search -> O(log n): Pencarian logaritmik berkinerja tinggi berdasarkan ID terurut."""
        low = 0
        high = len(sorted_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if sorted_list[mid]['id'] == target_id:
                return sorted_list[mid]
            elif sorted_list[mid]['id'] < target_id:
                low = mid + 1
            else:
                high = mid - 1
        return None