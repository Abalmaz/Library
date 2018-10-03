let vm = new Vue({
   el: '#library',
   delimiters: ['[[', ']]'],
   data: {
       books: [],
       loading: false,
       currentBook: {},
       message: null
   },
   mounted: function() {
        this.getBooks();
   },
   methods: {
        getBooks: function() {
            this.loading = true;
            axios.get('/api/books/')
            .then((response) => {
                this.books = response.data;
                this.loading = false;
             })
            .catch((err) => {
               this.loading = false;
               console.log(err);
            })
        },
        getBook: function(id) {
            this.loading = true;
            axios.get('/api/books/'+id+'/')
            .then((response) => {
                this.currentBook = response.data;
                $("#BookModal").modal('show');
                this.loading = false;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        },
        getAuthors: function() {
            this.loading = true;
            axios.get('/api/authors/')
            .then((response) => {
                this.authors = response.data;
                this.loading = false;
             })
            .catch((err) => {
               this.loading = false;
               console.log(err);
            })
        },
        getAuthor: function(id) {
            this.loading = true;
            axios.get('/api/authors/${id}/')
            .then((response) => {
                this.currentAuthor = response.data;
                this.loading = false;
            })
            .catch((err) => {
                this.loading = false;
                console.log(err);
            })
        }
    }
})
