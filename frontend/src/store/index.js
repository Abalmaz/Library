import Vue from 'vue'
import Vuex from 'vuex'
import { Book } from '../api/books'

Vue.use(Vuex)

const state = {
  books: []
}

const getters = {
  books: state => state.books
}

const actions = {
  getBooks ({ commit }) {
    Book.list().then(books => {
      commit(SET_NOTES, { books })
    })
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions
})
