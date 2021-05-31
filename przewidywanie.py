import asyncio
import json
import numpy as np
import matplotlib.pyplot as plt
import aiohttp

from sklearn import preprocessing

from understat import Understat


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def results(team, kolejka, fixtures):
    wins = 0
    draws = 0
    losses = 0
    start = kolejka - 7
    if start < 0:
        start = 0
    matches = list()

    for game in fixtures:
        for side in ('h', 'a'):
            if game[side]['title'] == team:
                matches.append(game)

    for i in range(start, kolejka):
        game = matches[i]
        for side in ('h', 'a'):
            if game[side]['title'] == team:
                if game['goals']['h'] == game['goals']['a']:
                    draws += 1
                elif game['goals']['h'] > game['goals']['a']:
                    if side == 'h':
                        wins += 1
                    else:
                        losses += 1
                else:
                    if side == 'a':
                        wins += 1
                    else:
                        losses += 1
    return wins, draws, losses


def wynik(team, kolejka, fixtures):
    matches = list()
    for game in fixtures:
        for side in ('h', 'a'):
            if game[side]['title'] == team:
                matches.append(game)
    game = matches[kolejka]
    for side in ('h', 'a'):
        if game[side]['title'] == team:
            if side == 'h':
                stadion = 1
                przeciwnik = game['a']['title']
            else:
                stadion = 0
                przeciwnik = game['h']['title']
            if game['goals']['h'] == game['goals']['a']:
                return 0.5, przeciwnik, stadion
            elif game['goals']['h'] > game['goals']['a']:
                if side == 'h':
                    return 1, przeciwnik, stadion
                else:
                    return 0, przeciwnik, stadion
            else:
                if side == 'a':
                    return 1, przeciwnik, stadion
                else:
                    return 0, przeciwnik, stadion


def zbieranie_danych(teams_list, fixtures, start_k, stop_k):
    training_inputs = list()
    training_outputs = list()
    druzyny = list()
    liczba_meczy = 0
    for team in teams_list:
        for i in range(start_k, stop_k):
            liczba_meczy += 1 
            score, opponent, strona = wynik(team, i, fixtures)
            wins, draws, losses = results(team, i, fixtures)
            wins_op, draws_op, losses_op = results(opponent, i, fixtures)
            druzyny.append([team, opponent])
            training_inputs.append([wins, draws, losses, wins_op, draws_op, losses_op, strona])
            training_outputs.append(score)

    training_inputs = np.array(training_inputs)
    training_inputs = preprocessing.normalize(training_inputs)  # normalizujemy inputy
    training_outputs = np.array(training_outputs)
    training_outputs = np.reshape(training_outputs, (1, liczba_meczy))
    training_outputs = training_outputs.T
    return training_inputs, training_outputs, liczba_meczy, druzyny


def testing(fixtures, learning_rate, prog, data):
    teams_list = list()
    for game in fixtures:
        for side in ('h', 'a'):
            if game[side]['title'] not in teams_list:
                teams_list.append(game[side]['title'])

    training_inputs, training_outputs, liczba_meczy, druzyny1 = zbieranie_danych(teams_list, fixtures, 8, 25)
    test_inputs, test_outputs, test_meczy, druzyny2 = zbieranie_danych(teams_list, fixtures, 28, 38)

    synaptic_weights = 2 * np.random.random((7, 1)) - 1
    # print(synaptic_weights)
    # print(training_outputs)
    bledy = []
    for iteration in range(data):
        input_layer = training_inputs
        outputs = sigmoid(np.dot(input_layer, synaptic_weights))  # mnożenie skalarne macierzy
        error = training_outputs - outputs
        sum_error = sum(error)
        for i in sum_error:
            bledy.append(abs(i))

        adjustments = learning_rate * error * sigmoid_derivative(outputs)
        synaptic_weights += np.dot(input_layer.T, adjustments)

    print(bledy)
    plt.plot(bledy)
    plt.show()
    # print(synaptic_weights)
    # print('Outputs after training: ')
    predict_outputs = sigmoid(np.dot(test_inputs, synaptic_weights))
    licznik = 0
    for i in range(1, test_meczy):
        if prog >= predict_outputs[i] >= 1 - prog:
            prediction = 0.5
        elif predict_outputs[i] < 1 - prog:
            prediction = 0
        else:
            prediction = 1
        print(druzyny2[i - 1][0], "vs", druzyny2[i - 1][1])
        print("Faktyczny wynik:", test_outputs[i], "Przewidywany wynik:", predict_outputs[i], "\n") # raw
        #print("Faktyczny wynik:", test_outputs[i], "Przewidywany wynik:", prediction, "\n")
        if test_outputs[i] == prediction:
            licznik += 1

    return licznik / test_meczy


async def main():
    async with aiohttp.ClientSession() as session:
        year = 2019  # year = int(input("Podaj rok: "))

        understat = Understat(session)
        fixtures = await understat.get_league_results(
            "epl",
            year,

        )
        maks = 0
        lr = 0
        progi = 0
        suma = 0
        data = 0
        """for j in np.arange(0.05, 1, step=0.05):
            print("learning rate:", j, "\n")
            for m in np.arange(0.6, 0.9, step=0.05):
                print("prog:", m, "\n")
                for g in range(100, 1050, 100):
                    for i in range(1, 10):
                        suma += testing(fixtures, j, m, g)

                    x = suma / 9
                    if x > maks:
                        maks = x
                        lr = j
                        progi = m
                        data = g
                    suma = 0"""

        """print(data)
        print(lr)
        print(progi)"""
        """do_scattera = []
        for i in range(1, 100):
            wynik_testu = testing(fixtures, 0.6, 0.6, 400)
            suma += wynik_testu
            do_scattera.append(wynik_testu)

        plt.scatter(range(1, 100), do_scattera)
        plt.show()
        x = suma/99"""
        x = testing(fixtures, 0.6, 0.6, 400)
        print("Skuteczność:", round(x * 100, 2), "%")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
