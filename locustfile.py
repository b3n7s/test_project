import random

import locust.stats
from dotenv import load_dotenv
from locust import HttpUser, between, task

from services.agrohelper_client import auth_as_admin

locust.stats.PERCENTILES_TO_REPORT = [0.50, 0.95, 0.99]
locust.stats.PERCENTILES_TO_STATISTICS = [0.50, 0.95, 0.99]
locust.stats.PERCENTILES_TO_CHART = [0.50, 0.95, 0.99]
# Загружаем переменные окружения
load_dotenv()


class FarmerApiUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://agroservice.softdevcenter.ru"

    # Значения для фильтров (только значения без ключей)
    has_bind_agents_values = [0, 1]
    note_color_values = ["red", "green", "yellow"]
    region_values = [
        1000,
        1001,
        1002,
        1003,
        1004,
        1005,
        1006,
        1007,
        1008,
        1009,
        1010,
        1011,
        1012,
        1013,
        1014,
        1015,
        1016,
        1017,
        1018,
        1019,
        1020,
        1021,
        1022,
        1023,
        1024,
        1025,
        1026,
        1027,
        1028,
        1029,
        1030,
        1031,
        1032,
        1033,
        1034,
        1035,
        1036,
        1037,
        1038,
        1039,
        1040,
        1041,
        1042,
        1043,
        1044,
        1045,
        1046,
        1047,
        1048,
        1049,
        1050,
        1051,
        1052,
        1053,
        1054,
        1055,
        1056,
        1057,
        1058,
        1059,
        1060,
        1061,
        1062,
        1063,
        1064,
        1065,
        1066,
        1067,
        1068,
        1069,
        1070,
        1071,
        1072,
        1073,
        1074,
        1075,
        1076,
        1077,
        1078,
        1079,
        1080,
        1081,
        1082,
        1083,
        1084,
        1085,
        1086,
        1087,
    ]
    culture_values = [
        '1000',
        '1001',
        '1002',
        '1003',
        '1004',
        '1005',
        '1006',
        '1007',
        '1008',
        '1009',
        '1010',
        '1011',
        '1012',
        '1013',
        '1014',
        '1015',
        '1016',
        '1017',
        '1018',
        '1019',
        '1020',
        '1021',
        '1022',
        '1023',
        '1024',
        '1025',
        '1027',
        '1028',
    ]
    lab_confirmed_values = [0, 1]
    available_values = [0, 1]
    period_values = ["week", "month", "quarter", "year"]
    organizer_values = [
        'e68ca7a5-ae0e-4221-b4f3-1364dc14f923',
        'b3050455-8a19-4a85-bfdc-dc21ee2cd7ee',
        'bc2cc1d1-d426-4d03-b476-7927a4fbd582',
        '484323fa-ca67-4c44-9a23-81165cad349b',
        '6f692f34-e6ee-4b0b-8cad-04ec40e151a5',
        '05225a14-27c0-44ab-804d-6775389c9c03',
        '67d87e88-8c1e-4684-b94e-1bab104b55c4',
        '793d57e0-06ec-4b29-8aa6-f7b9072f9dd6',
        '4ff53c17-3f06-480a-a1ab-9bb6bd8ffc1b',
        '0d8d2539-6826-441a-9dd1-af24fa219da2',
        'c9f37af0-a41a-47f8-acd2-31cb0f31f815',
        '5f9cbf5b-078d-41e6-be6a-eb84c76875b9',
        '02a118e8-217d-4bc4-b3d3-f871ffe84c47',
        'c40e71b2-5c66-45e5-b0b2-26639ae5c87e',
        'a0301f37-c63c-4733-a1a6-e574c14ba746',
        '4450e3c8-6360-4d69-8e8e-c3f1e6bf2a42',
        'dc2bbb10-161c-4aeb-b756-347660ab1f1c',
        'b5595381-6db3-4930-9d45-bd39b181cd5b',
        '6e87cb39-d086-48d6-aa14-63a9de274ea1',
        'b6b41327-ff06-4ed3-b12b-23d8286a79f2',
        'f39bbefc-4e3d-4da8-bea2-a3de55a9ff6e',
        'a3c3a159-358e-442a-81cb-4960e56fbb98',
        '43f23c8a-64ba-4f74-a98c-5d356123c311',
        '37b3e05a-6773-4668-8bfd-f3c9adcfb0fa',
        '1c1af415-8881-4b09-b003-197df62b18aa',
        '38b543b6-6c10-4f94-aec6-b99e179caf3f',
        '7ba58c01-7d39-490c-aa53-3566bd2d266a',
        'ac98d7da-c66c-40fa-a5b2-24687098808b',
        '2eca457d-71d0-47f1-b0c0-f09d8e3bd173',
        'ffcc9258-1bde-41cb-8f6c-7fe7d73ca939',
        '3a105385-f027-4a66-8c7c-43b9b15454a9',
        '4f056f15-d69f-4739-8d66-c1f25a036ef9',
        'bfe7a20c-9ec2-4f59-a225-76010c06cd7f',
        '4115d42d-0be5-4776-a967-62bba794178a',
        '7ea2ea86-0a3b-48bd-b538-f9494fa56982',
        '74689e29-2852-4e82-a90b-fa53483163f8',
        '1d3e0135-50e1-4cf3-adab-a9323d0b730e',
    ]  # 3 случайных UUID для организаторов
    agent_values = [
        'cf382a11-1f46-45eb-8551-1904c972d7b4',
        'cbfff054-5e1d-4926-a418-04fc42f08a07',
        'e70a5920-69d7-4d00-bd23-43d415c08481',
        '5dbff43d-5523-447d-bac6-f47001d467e2',
        'be56ca75-15be-45e2-9036-e4d14374e2aa',
        '77ee3810-307a-41ca-a3b1-7c82f6afc249',
        '399bb2b9-6c7c-43e2-bd5b-0b77ad24cd9e',
        'fa99ba16-c418-4bb9-b9f9-e70c9efb28d7',
        '28e5826c-ed00-454a-8eac-cc4c8195a68a',
        '51707667-4739-4149-9cb8-3a963f07bea6',
        'd615593e-06c9-49b6-b1c4-3a1ab6403f4d',
        '03f39987-0338-41ca-87ff-9730d80978e1',
        '835a3c52-816b-43bc-b655-a3f8c6986f3b',
        '7182987a-9571-412b-8bfe-f8d744014fa8',
        'f3b82005-d45f-4986-aed1-780f2038d8f1',
        '62ee5501-b488-426e-b111-7d60b97b8ef5',
        'c94e820d-3d8c-494a-984e-5b6869ffa64e',
        '41ea772a-3350-4fb6-a771-3e4e745c207f',
        '1cedd34a-900e-4927-92ba-e8c45affeba1',
        '733f2faf-ebd8-48e4-b439-8af426db5eab',
        'b2803466-1184-43fb-a7d5-6f1f7fce2979',
        'fbaea3bb-a841-4004-9e82-bed5f81006ce',
        '51a455a6-2d25-462d-9197-c95faefdf891',
        '47816a9a-7768-49b0-aa29-0a6644086b1a',
        '089d005a-ba32-47a4-9af9-cbcca385f33a',
        '03fa3b16-10ea-4aa5-bf64-8e2f9354847f',
        '4a6282e4-6908-4142-b5c7-0be494c5d730',
        '63518f9c-52f7-4c95-93fc-aeb76545ea8e',
        '2cf58ebf-f3a7-40e2-9344-ebb44bf5258d',
        'e4ac8e9f-4d70-4e5b-afd7-41a1bee29c13',
        '61819f1e-e921-449f-b780-2b465f7181a5',
        'c53d3d1e-b710-4668-9d27-81f1e6de3900',
        '41bd631c-8e90-40c8-a725-c6276fcf19a6',
        '24ff8e68-0d5f-45a2-bfc2-9838cd84d6e6',
        '30b2c4b9-ca7b-47b6-a1fc-ee94ce3cf3cf',
        '9fcb3c63-26f4-461d-b11a-f4f0935340a3',
        'fb18d1df-4b32-4695-bc9d-1ce9f46b8e6f',
        '14811bf8-92ec-4100-9128-fac062f124d4',
        '127ec0ef-e5bc-4434-bf96-d7636eb1fa12',
        'd94b5948-fff5-43a6-a2bb-b7cf5a2b36d1',
        'bd31ee68-5c5b-46db-8790-f799036fd9d3',
        '639950fd-1f56-45c8-a1af-9af57fc5c944',
        'e2f8dd5a-798d-4184-abe5-6bc805c37fff',
        '82d43593-3227-43ab-9027-b44cc00bb1e0',
        'decc7da1-a83f-4844-97a1-244175123d24',
        '74baecf1-7c3d-44fd-857c-1ffd40f50330',
        '1f139c1d-9906-44ab-ae51-d59b1f3a9595',
        '35f39ba7-a0ed-41b6-ae2c-c58933d15942',
        '4a92b1ec-7161-417c-bf2a-aa2658faa2e1',
        '6bbed67a-9ffd-4d24-99b3-86ccc4d4e834',
        '21a61def-9e84-452d-b590-0bdcebeab62a',
        '59787c50-3102-4c70-bc0d-770b0f30a6b4',
        'cb554546-8056-4013-9f75-1cfb6e21cbad',
        '254116d5-af73-40d8-8523-cd6c46b4b2b7',
        '85662989-a570-465f-ae5a-85dc6f561653',
        'd67745eb-bd77-4f92-862d-ed81da0656b7',
        '765cb529-7a0a-4308-99f3-86199873c946',
        'e10aa165-9fbc-420e-a8a7-a12f6fc3f47c',
        'c9a8bdeb-4257-4c79-aaf2-96b597e5b743',
        '8bcc38c0-f661-4770-bc89-c3e68a668f1f',
        '5197f8c2-dcee-42f2-815a-f2a7d7386ac0',
        'cc66b2b5-64fb-4139-aa93-4145190f66fd',
        '5cf78c20-a9ee-418b-9138-c33ce94f8cee',
        '4c29da71-c481-4e4e-b6e7-c92424128314',
        'dc9717d8-b969-41df-a584-17b2e06342a6',
        '2f6f2620-0bb9-47c2-9466-d68c67de0b7b',
        '37222eba-3f56-4126-9caa-bea95b0723b0',
        '39be46d7-0175-4b4a-a967-fd92eb21c3ec',
        'a9903bb1-db7b-4141-a4c4-a957997eda8b',
        '706c5ae4-594b-4934-ae8a-480567fcf813',
        '0c2d1d3e-bdd5-44e3-8786-bd4ceb3ad9e8',
        'b126bea1-5549-4944-a11f-7f393dec83b2',
    ]  # 3 случайных UUID для агентов
    inn_status_values = [0, 1]

    def on_start(self):
        """Выполняется при старте каждого пользователя"""
        # Создаем и аутентифицируем клиент
        admin_token = auth_as_admin()

        self.client.headers = {'Authorization': admin_token.access_token}

    def get_random_filters(self, max_filters):
        """Генерация случайных фильтров в правильном формате"""
        all_possible_filters = {
            "has_bind_agents": random.choice(self.has_bind_agents_values),
            "note_color": random.choice(self.note_color_values),
            "region": random.choice(self.region_values),
            "culture": random.choice(self.culture_values),
            "lab_confirmed": random.choice(self.lab_confirmed_values),
            "available": random.choice(self.available_values),
            "created": random.choice(self.period_values),
            "modified": random.choice(self.period_values),
            "organizer": random.choice(self.organizer_values),
            "agent": random.choice(self.agent_values),
            "touch_date": random.choice(self.period_values),
            "inn_status": random.choice(self.inn_status_values),
        }

        # Выбираем случайное подмножество фильтров
        selected_filters = {}
        keys = list(all_possible_filters.keys())
        random.shuffle(keys)

        for key in keys[:max_filters]:
            value = all_possible_filters[key]
            if value is not None:  # Пропускаем None значения
                selected_filters[f"filter[{key}]"] = value

        return selected_filters

    @task(50)
    def simple_search(self):
        # Простые запросы с 1-3 фильтрами
        filters = self.get_random_filters(random.randint(1, 3))
        page = random.randint(1, 50)
        self.client.get("/api/farmers", params={**filters, "page": page})

    @task(30)
    def complex_search(self):
        # Средние запросы с 4-6 фильтрами
        filters = self.get_random_filters(random.randint(4, 6))
        page = random.randint(1, 200)
        self.client.get("/api/farmers", params={**filters, "page": page})

    @task(15)
    def heavy_search(self):
        # Сложные запросы с 7+ фильтрами
        filters = self.get_random_filters(random.randint(7, 12))
        page = random.randint(100, 500)
        self.client.get("/api/farmers", params={**filters, "page": page})

    @task(5)
    def pagination_stress_test(self):
        # Тестирование крайних случаев пагинации
        filters = self.get_random_filters(random.randint(3, 5))
        for page in [1, 2, 1000, 1874, 1875]:
            self.client.get("/api/farmers", params={**filters, "page": page})
            self.wait()


class AdminApiUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://agroservice.softdevcenter.ru"

    def on_start(self):
        """Выполняется при старте каждого пользователя"""
        # Создаем и аутентифицируем клиент
        admin_token = auth_as_admin()

        self.client.headers = {'Authorization': admin_token.access_token}

    @task(100)
    def simple_search(self):
        page = random.randint(1, 15)
        self.client.get("/api/admin/users", params={"page": page})
