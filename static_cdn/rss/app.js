var rssApp = new Vue({
        el: '#rss-app',

        data: {
                items: [],
                feeds: [],
                newLink: "",
                route: "feeds"
        },

        methods: {
                api: function(endpoint, method, data) {
                        var config = {
                                method: method || 'GET',
                                body: data !== undefined ? JSON.stringify(data) : null,
                                headers: {
                                        'content-type': 'application/json'
                                }
                        };

                        return fetch(endpoint, config)
                                        .then((response) => response.json())
                                        .catch((error) => console.log(error));
                },

                setup: function() {
                        var hash = window.location.hash;

                        if(hash) {
                                this.route = hash.slice(1);
                        }

                        this.reload();
                },

                reload: function() {
                        this.getItems();
                        this.getFeeds();
                },

                getFeeds: function() {
                        this.api("/rss/feeds/").then((feeds) => {
                                this.feeds = feeds;
                        });
                },

                getItems: function() {
                        this.api("/rss/items/").then((items) => {
                                this.items = items;
                        });
                },

                newFeed: function() {
                        this.api("/rss/feeds/", "POST", { url: this.newLink }).then(() => {
                                this.reload();
                        });
                },

                deleteFeed: function(id) {
                        this.api("/rss/feeds/" + id + "/", "DELETE").then(() => {
                                this.reload();
                        });
                },

                setRoute: function(route) {
                        this.route = route;
                }
        }
});