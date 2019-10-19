from exceptions.duplicate_item import DuplicateItem
class Validator:
    def check_duplicate_item(self, cars):
        res = {}
        duplicated = set()
        for car in cars:
            if car['Id'] in res:
                res[car['Id']] += 1
                duplicated.add(car['Id'])
            else:
                res[car['Id']] = 1

        if len(duplicated) > 0:
            duplicaters = []
            for x in duplicated:
                duplicaters.append((x, res[x]))
            raise DuplicateItem(str(list(duplicaters)))