import tp_unity_ai.tp as tp

if __name__ == '__main__':
    agent = tp.interactiveGraphics.get_agent_with_name('Ball')
    print(agent.name)
    print(agent.id)
    agent.move()
    agent.set_speed(100)
