# import sqlite3

# conn = sqlite3.connect('physics_resources.db')
# c = conn.cursor()

# # Create a table for resources
# c.execute('''CREATE TABLE resources 
#             (id INTEGER PRIMARY KEY AUTOINCREMENT,
#             topic_id INTEGER NOT NULL,
#             title TEXT NOT NULL,
#             filename TEXT NOT NULL,
#             filepath TEXT NOT NULL)''')

# # Create a table for topics
# c.execute('''CREATE TABLE topics
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#               topic_name TEXT NOT NULL)''')

# # Add topics to the topics table
# topics = [('Measurements and Uncertainties',),
#           ('Mechanics',),
#           ('Thermal Physics',),
#           ('Waves',),
#           ('Electricity and Magnetism',),
#           ('Circular Motion and Gravitation',),
#           ('Atomic, Nuclear and Particle Physics',),
#           ('Energy Production',),
#           ('Wave Phenomena',),
#           ('Fields',),
#           ('Electromagnetic Induction',),
#           ('Quantum and Nuclear Physics',)]

# c.executemany('INSERT INTO topics (topic_name) VALUES (?)', topics)

# # Commit changes and close the connection
# conn.commit()
# conn.close()