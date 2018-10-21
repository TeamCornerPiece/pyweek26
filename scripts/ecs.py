from scripts.components import *

ENT_ID, IS_ACTIVE = range(2)
DATA_START = 2


class ECS:
    def __init__(self):
        self.data = [{} for _ in range(COMP_COUNT + 1)]
        self.member_count = [0 for _ in range(COMP_COUNT + 1)]

    def add_entity(self):
        self.data[ENTITY][self.member_count[ENTITY]] = [-1 for _ in range(COMP_COUNT)]
        self.member_count[ENTITY] += 1
        return self.member_count[ENTITY] - 1

    def remove_entity(self, ent_id):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'
        if ent_id in self.data[ENTITY]:
            self.remove_components(ent_id)
            del self.data[ENTITY][ent_id]

    def get_entities(self, *comp_types: int):
        if comp_types:
            for ent_id, comp_ids in self.data[ENTITY].items():
                for comp_type in comp_types:
                    assert comp_type < COMP_COUNT, 'invalid component'
                    if comp_ids[comp_type] < 0:
                        break
                else:
                    yield ent_id
        else:
            return self.data[ENTITY].keys()

    def add_components(self, ent_id: int, *comp_types):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'
        for comp_type in comp_types:
            assert comp_type < COMP_COUNT, 'invalid component'
            comp_id = self.member_count[comp_type]
            self.data[comp_type][comp_id] = [ent_id, 1] + [-1 for _ in range(COMP_SIZES[comp_type])]
            self.data[ENTITY][ent_id][comp_type] = comp_id
            self.member_count[comp_type] += 1

    def remove_components(self, ent_id: int, *comp_types):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'

        if not comp_types:
            comp_types = range(COMP_COUNT)

        for comp_type in comp_types:
            assert comp_type < COMP_COUNT, 'invalid component'
            comp_id = self.data[ENTITY][ent_id][comp_type]
            if comp_id in self.data[comp_type]:
                del self.data[comp_type][comp_id]
            self.data[ENTITY][ent_id][comp_type] = -1

    def has_components(self, ent_id: int, *comp_types):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'

        for comp_type in comp_types:
            assert comp_type < COMP_COUNT, 'invalid component'
            if self.data[ENTITY][ent_id][comp_type] < 0:
                break
        else:
            return True

    def get_component_data(self, ent_id: int, comp_type: int):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'
        assert comp_type < COMP_COUNT, 'invalid component'
        comp_id = self.data[ENTITY][ent_id][comp_type]
        if comp_id >= 0:
            return self.data[comp_type][comp_id]

    def set_component_data(self, ent_id: int, comp_type: int, *attrs, **named_attrs):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'
        assert comp_type < COMP_COUNT, 'invalid component'

        comp_id = self.data[ENTITY][ent_id][comp_type]
        assert comp_id >= 0, 'entity does not have component of that type'

        for index, value in enumerate(attrs):
            self.data[comp_type][comp_id][index+2] = value
        for index, value in named_attrs.items():
            self.data[comp_type][comp_id][eval(index)] = value

    def set_active(self, ent_id: int, comp_type: int, active: bool):
        assert ent_id in self.data[ENTITY], 'invalid ent_id'
        assert comp_type < COMP_COUNT, 'invalid component'
        comp_id = self.data[ENTITY][ent_id][comp_type]
        self.data[comp_type][comp_id][IS_ACTIVE] = int(active)

    def set_data(self, data):
        self.data = data
        for data_type, values in enumerate(self.data):
            if values:
                self.member_count[data_type] = max(values.keys()) + 1
            else:
                self.member_count[data_type] = 0

    def clear_data(self):
        self.data = [{} for _ in range(COMP_COUNT + 1)]
        self.member_count = [0 for _ in range(COMP_COUNT + 1)]
