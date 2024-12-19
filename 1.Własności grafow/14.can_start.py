mission_control = {
    'FlightControl': ['Engine', 'Weather', 'Crew'],
    'Engine': ['Engine Temp', 'Fuel'],
    'Engine Temp': [],
    'Fuel': [],
    
}
status={
    'Engine Temp': True,
    'Fuel': True,
    'Wind': True,
    'Air Temp': True,
    'Clouds': True,
    'Communications': True,
    'Health': False
}

def can_start(graph,status, start_node)