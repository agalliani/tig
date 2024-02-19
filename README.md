Please note there are a couple variables in the above code you will want to change the influx password and grafana password environment variables. The grafana password will be prompted to change upon first login, so that one is not as critical.

I have caddy involved here to allow Grafana over HTTPS. Editing grafana.ini to allow HTTPS is possible, but a reverse proxy like Caddy makes this far easier.


We need to create some locally signed certificates for Caddy to use for HTTPS because without them, HTTPS isn’t a thing.

Create a grafana directory inside your tig directory

`cd ~/tig`

`mkdir grafana`

Now generate a new private key, a certificate signing request and finally sign that key.

`openssl genrsa -out grafana.key 2048`

`openssl req -new -key grafana.key -out grafana.csr`

`openssl x509 -req -days 3650 -in grafana.csr -signkey grafana.key -out grafana.crt`

Generating a new CSR will prompt you for a few answers. Just make sure to set the ‘common name’ to the URL you want to use in Caddy for serving up your Grafana page.

These are self-signed certificates, so they are not production ready. For a production environment it is necessary to use proper certs.


### Finally start your docker compose!
`cd ~/tig`

`docker compose up -d`



##### Testing

Publish some data on mosquitto:

`docker container exec mosquitto mosquitto_pub -t bedroom/temperature -m "bedroom_temperature celsius=20"`

Check on the db:

`docker exec -it influxdb influx`

`use telegraf`

`show series`



### Grafana example

Now that Grafana started it is listening on http://localhost:3000. Access it with your navigator. The default login infos are: admin / admin. Login and change your password if needed.

Let’s connect Grafana to InfluxDB. Go to http://localhost:3000/datasources. Add a new data source. In the data source providers options choose InfluxDB. Now, in the form, for the HTTP URL field write: http://influxdb:8086, the InfluxDB location on our Docker iot network. Scroll down, in InfluxDB details, in the database field write: telegraf. Save & test the data source, Grafana should tell you that the data source is working. Houra!

Now let’s create a new Grafana dashboard. Head to http://localhost:3000/dashboard/new. From here click the Add new panel button. At the bottom of the screen you will find the query editor. Edit the query:

`SELECT last("celsius") FROM "bedroom_temperature" WHERE $timeFilter GROUP BY time($__interval) fill(previous)`

Use the query you want to view your data. And that’s it. You can now query your InfluxDB database from Grafana. Querying InfluxDB is out of the scope of this article and as such I recommend that you read the documentation.

https://docs.influxdata.com/influxdb/v2/tools/grafana/




## Portainer on Linux

docker volume create portainer_data

docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest


https://localhost:9443