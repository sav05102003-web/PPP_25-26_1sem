import copy

class RecursionTracker:
    def __init__(self):
        self.history = []
        self.results = []
    
    def log_step(self, action, depth, partial_result, remaining_or_next):
        snapshot = {
            "action": action,                  
            "depth": depth,                    
            "current_partial": partial_result, 
            "context": remaining_or_next     
        }
        self.history.append(snapshot)

    def generate_permutations(self, elements, current_path=None):
        if current_path is None:
            current_path = []
            self.results = [] 
            self.history = []

      
        self.log_step("RECURSION_IN", len(current_path), current_path, elements)

        if not elements:
            self.results.append(current_path)
            self.log_step("RESULT_FOUND", len(current_path), current_path, "None")
            return

        for i in range(len(elements)):
            elem = elements[i]
            remaining_elements = elements[:i] + elements[i+1:]
            self.generate_permutations(remaining_elements, current_path + [elem])
        self.log_step("BACKTRACKING", len(current_path), current_path, "Returning up")

    def generate_combinations(self, elements, k, start_index=0, current_path=None):
        if current_path is None:
            current_path = []
            self.results = []
            self.history = []

        self.log_step("RECURSION_IN", len(current_path), current_path, f"Start Index: {start_index}")

        if len(current_path) == k:
            self.results.append(current_path)
            self.log_step("RESULT_FOUND", len(current_path), current_path, "None")
            return

        for i in range(start_index, len(elements)):
            elem = elements[i]
            
            self.generate_combinations(elements, k, i + 1, current_path + [elem])

        self.log_step("BACKTRACKING", len(current_path), current_path, "Returning up")


raw_input = input(" Введите элементы через пробел (например: A B C 1 2): ")
input_data= raw_input.split()


print("--- Генерация Перестановок ---")
perm_tracker = RecursionTracker()
perm_tracker.generate_permutations(input_data)

print(f"Всего перестановок: {len(perm_tracker.results)}")
print("Итоговые результаты:", perm_tracker.results)

print("\n--- Пример анализа истории  ---")
for step in perm_tracker.history[0:]:
    print(step)
