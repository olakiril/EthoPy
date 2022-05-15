import pygame
from core.Interface import *


class DummyPorts(Interface):
    def __init__(self, **kwargs):
        super(DummyPorts, self).__init__(**kwargs)
        pygame.init()
        self.dummy_ports = {'left_port'       : [pygame.KEYDOWN, pygame.K_LEFT],
                            'right_port'      : [pygame.KEYDOWN, pygame.K_RIGHT],
                            'proximity_true'  : [pygame.KEYDOWN, pygame.K_SPACE],
                            'proximity_false' : [pygame.KEYUP, pygame.K_SPACE]}

    def in_position(self):
        self.__get_events()
        ready_dur = self.timer_ready.elapsed_time() if self.ready else self.ready_dur
        return self.ready, ready_dur, self.ready_tmst

    def __get_events(self):
        port = 0
        events = pygame.event.get() if pygame.get_init() else []

        for event in events:
            # Check if any port is licked
            port = self._port_activated(event, port)

            # Check position
            self._proximity_change(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
                self.logger.update_setup_info({'status': 'stop'})
        return port

    def _port_activated(self, event, port):
        if self.dummy_ports_true(event, 'left_port'):
            print('Probe 1 activated!')
            port = 1
        if self.dummy_ports_true(event, 'right_port'):
            print('Probe 2 activated!')
            port = 2
        if port:
            port = self.ports[Port(type='Lick', port=port) == self.ports][0]
            self.resp_tmst = self.beh.log_activity(port.__dict__)
        return port

    def _proximity_change(self, event):
        if self.dummy_ports_true(event, 'proximity_true') and not self.ready:
            self.ready = True
            port = self.ports[Port(type='Proximity', port=1) == self.ports][0]
            self.resp_tmst = self.beh.log_activity({**port.__dict__, 'in_position': self.ready})
            print('in position')
        elif self.dummy_ports_true(event, 'proximity_false') and self.ready:
            self.ready = False
            port = self.ports[Port(type='Proximity', port=1) == self.ports][0]
            tmst = self.beh.log_activity({**port.__dict__, 'in_position': self.ready})
            self.ready_dur = tmst - self.ready_tmst
            print('off position')
            print(pygame.mouse.get_pos())

    def dummy_ports_true(self, event, name):
        if event.type == self.dummy_ports[name][0]:
            if event.key == self.dummy_ports[name][1]:
                return True
        return False

    def load_calibration(self):
        pass

    def calc_pulse_dur(self, reward_amount):
        actual_rew = dict()
        for port in self.rew_ports:
            actual_rew[port] = reward_amount
        return actual_rew

    def cleanup(self):
        self.set_running_state(False)
        self.logging = False
        if self.exp.sync:
            self.closeDatasets()
