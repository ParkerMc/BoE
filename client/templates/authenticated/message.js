Template.message.helpers({
  name( userId ) {
    if ( userId ) {
      let user = Meteor.users.findOne( userId, { fields: { 'profile.name': 1 } } );
      return user ? `${ user.profile.name }` : '';
    }
  },
  username( userId ) {
    if ( userId ) {
      let user = Meteor.users.findOne( userId, { fields: { 'username': 1 } } );
      return user ? `${ user.username }` : '';
    }
  }
});

Template.message.events({
  'click a' ( event ) {
    event.preventDefault();
    window.open( event.target.href, '_blank' );
  }
});
