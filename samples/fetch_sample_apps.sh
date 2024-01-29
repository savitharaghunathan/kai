pushd .
mkdir -p sample_repos
cd sample_repos || exit
### Java EE to Quarkus examples
# 'master' is original Java EE (forked from: https://github.com/deewhyweb/eap-coolstore-monolith.git)
# 'quarkus-migration' is the code migrated to Quarkus
git clone https://github.com/mathianasj/eap-coolstore-monolith.git
cd eap-coolstore-monolith || exit
# Our unit tests will assume that the quarkus-migration branch has been linked in this checkout
git checkout quarkus-migration
cd ..

### KitchenSink
##### https://github.com/konveyor/example-applications/issues/19
########## https://github.com/jboss-developer/jboss-eap-quickstarts/tree/7.4.x/kitchensink
#git clone https://github.com/jboss-developer/jboss-eap-quickstarts.git jboss-eap-quickstarts-javaee
########## https://github.com/tqvarnst/jboss-eap-quickstarts/tree/quarkus-3.2/kitchensink
## https://github.com/tqvarnst/jboss-eap-quickstarts/tree/quarkus-3.2
# We will soon copy the below kitchensink example to Chris repo at: https://github.com/christophermay07/quarkus-migrations
git clone https://github.com/tqvarnst/jboss-eap-quickstarts.git kitchensink-quarkus
cd kitchensink-quarkus || exit
git checkout quarkus-3.2
cd ..

# Ticket Monster
# 'master' is original Java EE
# 'quarkus' is quarkus migration
git clone https://github.com/jmle/monolith.git ticket-monster

# We are assuming the jboss-eap-quickstart examples we will use come have a starting point of the 7.4.x branch
# '7.4.x' original branch
git clone https://github.com/jboss-developer/jboss-eap-quickstarts
cd jboss-eap-quickstarts || exit
git checkout 7.4.x
cd ..

# 'main' is the branch we will use for the quarkus migration
git clone https://github.com/christophermay07/quarkus-migrations jboss-eap-quickstarts-quarkus

# HelloWorld MDB
#  This started from: https://github.com/jboss-developer/jboss-eap-quickstarts/tree/7.4.x/helloworld-mdb/src/main/java/org/jboss/as/quickstarts/mdb
git clone https://github.com/savitharaghunathan/helloworld-mdb.git helloworld-mdb-quarkus
cd helloworld-mdb-quarkus || exit
git checkout quarkus
cd ..

popd || exit
