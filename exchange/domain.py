from exchange.models import Participant, Exchange


def start_exchange(party):
    exchange_list = []
    party.status = "started"
    party.save()
    participants = list(Participant.objects.filter(party=party, status='Joined'))
    for counter, participant in enumerate(participants):
        exchange = Exchange.objects.create(giver=participant, receiver=participants[counter-1], party=party)
        exchange_list.append(exchange)
    return party, exchange_list
