
def triggerEvent(event):
    return event.get('trigger_state', '')

def shouldTriggerEvent(event, condition):
    ev_condition = event.get('condition', {})
    same_state = ev_condition.get('state', None) == condition.get('state', None)
    same_value = ev_condition.get('value', None) == condition.get('value', None)

class EventManager:
    eventList = []

    def addEvent(self, event):
        self.eventList.append(event)

    def runOnce(self, state):
        updateStateList = []
        [
            triggerEvent(event)
            for event in self.eventList
            if shouldTriggerEvent(event, state)
        ]
        return updateStateList

