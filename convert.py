import os
import sys
import sqlite3

######################################
# Helper functions

def safeMakeDir(d):
  if os.path.exists(d):
    return
  os.makedirs(d)

def setDir(d):
  safeMakeDir(d)
  os.chdir(d)

######################################
# Let's do shit

if not len(sys.argv) == 2:
  print 'Please provide exactly 1 parameter - the mbtiles input filename'
  exit()

# Process input
input_filename = sys.argv[1]
dirname = input_filename[0:input_filename.index('.')]
print 'Converting file "%s" into tiles in local directory "%s"' % (input_filename, dirname)

# This will fail if there is already a directory.
# I could make a better error message, but I intend for this to fail,
# because it's better to not delete data.
os.makedirs(dirname)

# Database connection boilerplate
connection = sqlite3.connect(input_filename)
cursor = connection.cursor()

# The mbtiles format helpfully provides a table that aggregates all necessary info
cursor.execute('select * from tiles')

os.chdir(dirname)
for row in cursor:
  setDir(str(row[0]))
  setDir(str(row[1]))
  # TODO: Should we support jpg too?
  output_file = open(str(row[2]) + '.png', 'w')
  output_file.write(row[3])
  output_file.close()
  os.chdir('..')
  os.chdir('..')

print 'Done!'
