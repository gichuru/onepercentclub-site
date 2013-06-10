
/*
 Models
 */

App.ProjectCountry = DS.Model.extend({
    name: DS.attr('string'),
    subregion: DS.attr('string')
});

App.ProjectPitch = DS.Model.extend({
    url: 'projects/pitches',

    project: DS.belongsTo('App.MyProject'),
    created: DS.attr('date'),
    status: DS.attr('string'),

    // Basics
    title: DS.attr('string'),
    pitch: DS.attr('string'),
    theme: DS.attr('string'),
    tags: DS.hasMany('App.Tag'),
    description: DS.attr('string'),
    need: DS.attr('string'),

    // Location
    country: DS.belongsTo('App.ProjectCountry'),
    latitude: DS.attr('number'),
    longitude: DS.attr('number'),

    // Media
    image: DS.attr('string'),
    image_small: DS.attr('string'),
    image_square: DS.attr('string'),
    image_bg: DS.attr('string')

});


App.ProjectPlan = DS.Model.extend({
    url: 'projects/plans',

    project: DS.belongsTo('App.MyProject'),
    status: DS.attr('string'),
    created: DS.attr('date'),

    // Basics
    title: DS.attr('string'),
    pitch: DS.attr('string'),
    theme: DS.attr('string'),
    need: DS.attr('string'),
    tags: DS.hasMany('App.Tag'),

    // Description
    description: DS.attr('string'),
    effects: DS.attr('string'),
    future: DS.attr('string'),
    for_who: DS.attr('string'),
    reach: DS.attr('number'),

    // Location
    country: DS.belongsTo('App.ProjectCountry'),
    latitude: DS.attr('number'),
    longitude: DS.attr('number'),

    // Media
    image: DS.attr('string'),
    image_small: DS.attr('string'),
    image_square: DS.attr('string'),
    image_bg: DS.attr('string')

});


App.Project = DS.Model.extend({
    url: 'projects',

    // Model fields
    slug: DS.attr('string'),
    title: DS.attr('string'),
    phase: DS.attr('string'),
    created: DS.attr('date'),

    pitch: DS.belongsTo('App.ProjectPitch'),
    plan: DS.belongsTo('App.ProjectPlan'),

    owner: DS.belongsTo('App.UserPreview'),
    team_member: DS.belongsTo('App.UserPreview'),

    money_asked: DS.attr('number'),
    money_donated: DS.attr('number'),

    days_left: DS.attr('number'),
    supporters_count: DS.attr('number'),

    wallposts: DS.hasMany('App.WallPost'),


    money_needed: function(){
        var donated = this.get('money_asked') - this.get('money_donated');
        if (donated < 0) {
            return 0;
        }
        return Math.ceil(donated);
    }.property('money_asked', 'money_donated'),

});


App.ProjectPreview = App.Project.extend({

});

/*
 Controllers
 */


App.ProjectController = Em.ObjectController.extend({
    isFundable: function(){
        return this.get('phase') == 'Fund';
    }.property('phase')

});


App.ProjectSupporterListController = Em.ArrayController.extend({
    supportersLoaded: function(sender, key) {
        if (this.get(key)) {
            this.set('model', this.get('supporters').toArray());
        } else {
            // Don't show old content when new content is being retrieved.
            this.set('model', null);
        }
    }.observes('supporters.isLoaded')

});


/*
 Views
 */

App.ProjectMembersView = Em.View.extend({
    templateName: 'project_members'
});

App.ProjectSupporterView = Em.View.extend({
    templateName: 'project_supporter',
    tagName: 'li',
    didInsertElement: function(){
        this.$('a').popover({trigger: 'hover', placement: 'top', width: '100px'})
    }
});

App.ProjectSupporterListView = Em.View.extend({
    templateName: 'project_supporter_list'
});

App.ProjectListView = Em.View.extend({
    templateName: 'project_list'
});


App.ProjectView = Em.View.extend({
    templateName: 'project',

    didInsertElement: function(){
        this.$('#detail').css('background', 'url("' + this.get('controller.image_bg') + '") 50% 50%');
        this.$('#detail').css('background-size', '100%');

        // TODO: The 50% dark background doesn't work this way. :-s
        this.$('#detail').css('backgroundColor', 'rgba(0,0,0,0.5)');

        var donated = this.get('controller.money_donated');
        var asked = this.get('controller.money_asked');
        this.$('.donate-progress').css('width', '0px');
        var width = 0;
        if (asked > 0) {
            width = 100 * donated / asked;
            width += '%';
        }
        this.$('.donate-progress').animate({'width': width}, 1000);
    }
});

