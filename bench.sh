age: ./bench.sh <host> <reps>
HOST=$1
REPS=$2
for cmd in add rawImage dotProduct jsonImage; do
	  echo "== REST $cmd"
	    uv run python rest-client.py $HOST $cmd $REPS | tail -1
	      echo "== gRPC $cmd"
	        uv run python grpc-client.py $HOST $cmd $REPS | tail -1
	done
	echo "== PING"
	ping -c 10 $HOST | tail -1
