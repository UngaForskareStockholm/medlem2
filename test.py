import lib.database
lib.database.db.connect(host="10.11.11.24", database="dev_medlem2", username="postgres")
import model.bylaw
import model.user
import model.address

#__builtins__.db=db

params=dict()
params['bylaw']='asd'
params['created_by']=0
m=model.bylaw.Bylaw.create(params)

print "asd", m['bylaw']

m['bylaw'] = "aoieusth8isuey4zhj8rifu4hkr"

print "aoieusth8isuey4zhj8rifu4hkr", m['bylaw']

u=model.user.User(0)

print "admin", u['name']

print "True", u.authenticate("admin")

print "None", u.set_password("asd")

print "False", u.authenticate("admin")

print "None", u.set_password("admin")

print "True", u.authenticate("admin")

params=dict()
params['address_line1']=''
params['address_line2']=''
params['postal_code']=''
params['town']=''
params['created_by']=0
a=model.address.Address.create(params)
