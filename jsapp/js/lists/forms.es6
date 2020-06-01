import React from 'react';
import PropTypes from 'prop-types';
import reactMixin from 'react-mixin';
import Reflux from 'reflux';

import {searches} from '../searches';
import {actions} from '../actions';
import {stores} from '../stores';
import mixins from '../mixins';
import SearchCollectionList from '../components/searchcollectionlist';

import {hashHistory} from 'react-router';
import { SINGLE_FORM } from '../constants';

class FormsSearchableList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchContext: searches.getSearchContext('forms', {
        filterParams: {
          assetType: 'asset_type:survey',
        },
        filterTags: 'asset_type:survey',
      })
    };
  }
  componentDidMount () {
    this.searchSemaphore();
    if(SINGLE_FORM){
      if(stores.allAssets.data.length>0)
        hashHistory.replace(`/forms/${stores.allAssets.data[0].uid}`)
      else
        this.listenTo(actions.search.assets.completed, this.onListAssetsCompleted);
    }
  }
  
  onListAssetsCompleted(searchData, response) {
    if(response.results.length>0){
      this.setState({assetID: response.results[0].uid});
      hashHistory.replace(`/forms/${response.results[0].uid}`)
    }
  }



  render () {
    return (
      <SearchCollectionList
        showDefault
        searchContext={this.state.searchContext} />
      );
  }
}

FormsSearchableList.contextTypes = {
  router: PropTypes.object
};

reactMixin(FormsSearchableList.prototype, searches.common);
reactMixin(FormsSearchableList.prototype, mixins.droppable);
reactMixin(FormsSearchableList.prototype, Reflux.ListenerMixin);

export default FormsSearchableList;
