# generates a bunch of users to test out
# the rendering of the list of other players

for i in {0..1000}
do
  curl -s -F "user=testUser$i" http://192.168.0.152:5000/login > /dev/null &
done
