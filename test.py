import lib.database
lib.database.db.connect(host="10.11.11.24", database="dev_medlem2", username="postgres")
import model.bylaw
import model.user
import model.address

#__builtins__.db=db

params=dict()
params['bylaw']='asd'
m=model.bylaw.Bylaw.create(params, 0)

print m['bylaw']

m['bylaw'] = "aoieusth8isuey4zhj8rifu4hkr"

print m['bylaw']

u=model.user.User(0)

print u['name']

print u.authenticate("admin")

print u.set_password("asd")

print u.authenticate("admin")

print u.set_password("admin")

print u.authenticate("admin")

params=dict()
params['email']=''
params['phone']=''
params['address_line1']=''
params['address_line2']=''
params['postal_code']=''
params['town']=''
a=model.address.Address.create(params, 0)
