import copy


def get_all_moves(game_field, player_one, player_two, path):
    game_fields = []
    tem_field = copy.deepcopy(game_field)
    tem_player = copy.deepcopy(player_one)
    tem_two_player = copy.deepcopy(player_two)
    tem_player.set_places_to_move(game_field, [tem_player, tem_two_player])
    ind = get_all_step(tem_player, path)
    tem_player.set_next_position(tem_player.places_to_move[ind])
    if tem_player.can_move_here:
        tem_field.move_player(tem_player)
        game_fields.append(
            (tem_field, tem_player, tem_two_player, tem_player.next_position))
    return game_fields


def get_all_step(player, path):
    ind = -1
    for index, step in enumerate(player.places_to_move):
        if step.x == path[2][1] and step.y == path[2][0]:
            ind = index
            break

    return ind
