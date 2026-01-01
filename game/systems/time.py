class TimeSystem:
    MS_TICK = 6
    
    def __init__(self):
        pass

    def update(self, state):
        ms_total = self.MS_TICK + state.miliseconds

        if ms_total >= 60:
            state.miliseconds = ms_total - 60
            state.time[1] += ms_total // 60

            if state.time[1] >= 60:
                state.time[1] = 60 - state.time[1]
                state.time[0] += 1

                if state.time[0] == 13:
                    state.time[0] = 1
        else:
            state.miliseconds += self.MS_TICK