import seed from 'meteor/themeteorchef:seeder';

let _seedUsers = () => {
  Seed( 'users', {
    environments: [ 'development', 'staging', 'production' ],
    data: [{
      username: 'admin',
      email: 'admin@admin.com',
      password: 'password',
      profile: {
        name: 'Admin'
      },
      roles: [ 'admin' ]
    }]
  });
};

let _seedChannels = () => {
  Seed( 'channels', {
    environments: [ 'development', 'staging', 'production' ],
    data: [ { name: 'general' } ]
  });
};

export default function() {
  _seedUsers();
  _seedChannels();
}
