import tp_unity_ai.tp as tp
import time

if __name__ == '__main__':
    agent = tp.interactiveGraphics.get_agent_with_name('Cylinder')
    print(agent.name)
    print(agent.id)
    agent.move()
    time.sleep(0.3)
    agent.turn_left()
    time.sleep(2.9)
    agent.turn_right()
    time.sleep(3.5)
    agent.turn_right()
    agent.set_speed(15)
    time.sleep(2)
    agent.stop()
