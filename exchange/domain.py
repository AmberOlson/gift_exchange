from exchange.models import Participant, Exchange, Party


def start_exchange(party):
    exchange_list = []
    party.status = Party.STARTED
    party.save()

    if Exchange.objects.filter(party=party):
        # return 'exchanges not created'
        raise Exception('exchanges already created')
    participants = list(Participant.objects.filter(party=party, status=Participant.JOINED))
    for counter, participant in enumerate(participants):
        exchange = Exchange.objects.create(giver=participant, receiver=participants[counter - 1], party=party)
        exchange_list.append(exchange)
    return party, exchange_list
