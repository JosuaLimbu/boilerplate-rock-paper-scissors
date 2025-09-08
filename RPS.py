# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(last_opponent_move="", opp_moves=[], detected_bot=[], my_moves=[], freq_tracker=[{
    "RR": 0, "RP": 0, "RS": 0,
    "PR": 0, "PP": 0, "PS": 0,
    "SR": 0, "SP": 0, "SS": 0,
}]):
    # store opponent moves
    opp_moves.append(last_opponent_move)

    # basic counter dictionary
    counter_map = {"R": "P", "P": "S", "S": "R"}
    choice = "R"
    turn = len(opp_moves)

    # reset after 1000 rounds (avoids memory overflow)
    if turn == 1001:
        opp_moves.clear()
        detected_bot.clear()
        my_moves.clear()
        opp_moves.append(last_opponent_move)

    # identify opponent during first 3 rounds
    if turn <= 4:
        if turn == 1:
            my_moves.append("R")
            return "R"
        elif turn == 2:
            my_moves.append("P")
            return "P"
        elif turn == 3:
            my_moves.append("S")
            return "S"
        else:
            # detect bot by move pattern
            pattern = "".join(opp_moves[-3:])
            bot_lookup = {
                "RPP": "quincy",
                "PPP": "abbey",
                "PPS": "kris",
                "RRR": "mrugesh"
            }
            if pattern in bot_lookup:
                detected_bot.append(bot_lookup[pattern])

    # if bot not identified yet, just play a default move
    if not detected_bot:
        choice = "R"
    else:
        opponent = detected_bot[-1]

        # strategy against Quincy → predictable repeating sequence
        if opponent == "quincy":
            seq = ["R", "R", "P", "P", "S"]
            predicted = seq[turn % len(seq)]
            choice = counter_map[predicted]

        # strategy against Abbey → based on transition frequency
        elif opponent == "abbey":
            if len(my_moves) >= 2:
                seq_pair = "".join(my_moves[-2:])
                freq_tracker[0][seq_pair] += 1

            candidates = [
                my_moves[-1] + "R",
                my_moves[-1] + "P",
                my_moves[-1] + "S",
            ]
            scores = {k: freq_tracker[0][k] for k in candidates}
            prediction = max(scores, key=scores.get)[-1]
            choice = counter_map[counter_map[prediction]]

        # strategy against Kris → always counters our previous move
        elif opponent == "kris":
            predicted = counter_map[my_moves[-1]]
            choice = counter_map[predicted]

        # strategy against Mrugesh → counters our most frequent move in last 10 rounds
        elif opponent == "mrugesh":
            recent = my_moves[-10:]
            if not recent:
                common = "S"
            else:
                common = max(set(recent), key=recent.count)
            predicted = counter_map[common]
            choice = counter_map[predicted]

    my_moves.append(choice)
    return choice
