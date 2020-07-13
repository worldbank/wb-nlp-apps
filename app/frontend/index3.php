<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>NLP</title>

    <!-- <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"> -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <!-- <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script> -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- development version, includes helpful console warnings -->
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tagsinput/0.8.0/bootstrap-tagsinput.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tagsinput/0.8.0/bootstrap-tagsinput.css">

    <!-- https://www.nationsonline.org/oneworld/country_code_list.htm -->
    <link rel="stylesheet" type="text/css" href="css/flags-all.css">

    <script type="text/javascript" src="js/maps.js"></script>

    <style>
      .bg-custom{
        background:#2196F3!important;
      }

      .search-container{background:#3F51B5;}
      .document-row{
        margin-top:15px;
        padding-bottom:10px;
        margin-bottom:15px;
        border-bottom:1px solid gainsboro;
      }
      .document-icon{
        font-size:60px;
        color:#009688;
        font-weight:bold;
        padding:10px;
      }

      .document-row pre{
        background:#9e9e9e38;
        padding:10px;
      }

      .document-row .btn-sm{
        padding: .1rem .5rem;
        font-size: .875rem;
        line-height: 1.3;
      }
      .document-actions{
        margin-top:15px;
      }

      .xcustom-file-input{
        background: white;
        width: 90%;
      }
      .form-file-upload{
        width:100%;
      }

      .bg-gray{color:gray;}

      [v-cloak] {
        display:none;
      }

    </style>

  </head>

  <body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-custom">
      <a class="navbar-brand" href="#">NLP</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Similar documents</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="http://wbes2474/dfr" target="_blank">DFR Browser</a>
          </li>
        </ul>
        <span class="navbar-text">About
        </span>
      </div>
    </nav>

    <div class="body-container" id="app" v-cloak>
      <div class="container-fluid search-container" style="padding-top:50px">


        <div class="container">
          <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li v-on:click="function() {uploaded_doc_topics = null; togglePanels(false, false);}" class="nav-item">
              <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">Search</a>
            </li>
            <li v-on:click="togglePanels(false, false)" class="nav-item">
              <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Upload a file</a>
            </li>
            <li v-on:click="function() {togglePanels(false, true); if (topic_shares && topic_share_active) {plotStack(topic_shares);}}" class="nav-item">
            <!-- <li v-on:click="function() {togglePanels(false, true);}" class="nav-item"> -->
              <a class="nav-link" id="topic-share-tab" data-toggle="tab" href="#topic-share" role="tab" aria-controls="topic-share" aria-selected="false">Topic share explorer</a>
            </li>
            <li v-on:click="function() {findTopicMap(); togglePanels(true, false);}" class="nav-item">
              <a class="nav-link" id="topic-map-tab" data-toggle="tab" href="#topic-map" role="tab" aria-controls="topic-map" aria-selected="false">Topic map</a>
            </li>
          </ul>

          <div class="tab-content" id="myTabContent">
            <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab" style="padding:20px;">
              <!-- search -->
              <div class="form-row">
                <div class="col-10">
                  <input type="text"  v-on:keyup.enter="doSearch"  v-model="keywords" class="form-control" id="formGroupExampleInput" placeholder="Keywords">
                </div>
                <div class="col-2">
                  <button v-on:click="doSearch" type="button" class="btn btn-primary mb-2" v-bind:class="{ disabled: (isReady() && keywords.length != 0) === false }">Submit</button>
                </div>
              </div>
            </div>

            <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab" style="padding:20px;">
              <div class="input-group mb-3">
                <div class="custom-file">
                  <form class="form-file-upload" method="post" enctype="multipart/form-data" action="http://wbes2474:8910/api/related_docs">
                    <input type="file" ref="file" name="file" class="xcustom-file-input" id="xinputGroupFile01">
                    <!--<label class="custom-file-label" for="inputGroupFile01">Choose file</label>-->
                    <input type="submit" v-on:click="uploadFile" :disabled="isReady() === false"/>
                  </form>
                </div>
              </div>
            </div>

            <div class="tab-pane fade" id="topic-share" role="tabpanel" aria-labelledby="topic-share-tab" style="padding:20px;">
              <div class="form-row">
                <div class="col-10">
                </div>
                <div class="col-2">
                </div>
              </div>
            </div>

            <div class="tab-pane fade" id="topic-map" role="tabpanel" aria-labelledby="topic-map-tab" style="padding:20px;">
              <div class="form-row">
                <div class="col-10">
                </div>
                <div class="col-2">
                </div>
              </div>
            </div>

            <ul class="nav">
              <li class="nav-item">
                <div class="dropdown" style='padding-left:20px; padding-bottom:20px;'>
                  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Corpus {{" " + corpus_id}}</button>
                  <ul class="dropdown-menu multi-level" aria-labelledby="dropdownMenuButton">
                    <li class="dropdown-item" v-for="_corpus_id in corpus_ids" v-on:click="setCorpus(_corpus_id)">{{_corpus_id}}</li><!-- word2vec_models[corpus_id]}}</a> -->
                  </ul>
                </div>
              </li>
              <li class="nav-item" v-show="corpus_id != ''">
                <div class="dropdown" style='padding-left:20px; padding-bottom:20px;'>
                  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Sub-corpus {{" " + partition}}</button>
                  <ul class="dropdown-menu multi-level" aria-labelledby="dropdownMenuButton">
                    <li class="dropdown-item" v-for="(_models, partition) in models.WORD2VEC[corpus_id]" v-on:click="setPartition(partition)">{{partition}}</li><!-- word2vec_models[corpus_id]}}</a> -->
                  </ul>
                </div>
              </li>
              <li class="nav-item" v-if="(partition != '') && (!topic_share_active && !topic_map_active)">
                <div class="dropdown" style='padding-left:20px; padding-bottom:20px;'>
                  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Word2vec Model {{" " + word2vec_model_id}}</button>
                  <ul class="dropdown-menu multi-level" aria-labelledby="dropdownMenuButton">
                    <li class="dropdown-item" v-for="_item in models.WORD2VEC[corpus_id][partition]" v-on:click="setModel(_item.model_id, 'word2vec')">{{_item.model_id}}</li>
                  </ul>
                </div>
              </li>

              <li class="nav-item" v-if="(partition != '') && (corpus_id in models.LDA) && (partition in models.LDA[corpus_id])">
                <div class="dropdown" style='padding-left:20px; padding-bottom:20px;'>
                  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  LDA Model {{" " + lda_model_id}}</button>
                  <ul class="dropdown-menu multi-level" aria-labelledby="dropdownMenuButton">
                    <li class="dropdown-item" v-for="_item in models.LDA[corpus_id][partition]" v-on:click="setModel(_item.model_id, 'lda')">{{_item.model_id}}</li>
                  </ul>
                </div>
              </li>

              <li class="nav-item" v-if="(lda_model_id != '') && topic_share_active && ((topic_share_selected_adm_regions.length > 0) || (topic_share_selected_doc_types.length > 0) || (topic_share_selected_lending_instruments.length > 0))">
                <div style='padding-left:20px; padding-bottom:20px;'>
                  <button v-on:click='findTopicShare' class="btn btn-primary" type="button">Plot topic shares</button>
                </div>
              </li>

              <li class="nav-item" v-if="(lda_model_id != '') && topic_map_active">
                <div style='padding-left:20px; padding-bottom:20px;'>
                  <button v-on:click='findTopicMap' class="btn btn-primary" type="button">Plot topic map</button>
                </div>
              </li>

            </ul>

            <div v-if="(lda_model_id != '') && (topic_share_active || topic_map_active) && current_lda_model_topics" class="row" style="padding-left: 20px;">
              <div class="col-md-6">
                <div class="form-group">
                  <select class="form-control" id='topic_id' v-model="topic_id">
                    <option v-for="topic in current_lda_model_topics" :value="topic.topic_id">Topic {{ topic.topic_id }}: {{ topic.topic_words.map(function (x) {return x.word}).join(', ') }}</option>
                  </select>
                </div>
              </div>

              <div v-show="topic_share_active" class="col-md-6">
                <div class="button-group">
                  <button type="button" class="btn btn-light dropdown-toggle" data-toggle="dropdown">Data Partitions</button>
                  <ul class="dropdown-menu">
                    <li style="padding-left: 10px; padding-right: 10px;">
                      <span>Admin Region</span>
                    </li>
                    <li v-for="adm_reg in adm_regions" style="padding-left: 10px; padding-right: 10px;">
                      <label class="dropdown-menu-item checkbox">
                        <input type="checkbox" :value="adm_reg" v-model="topic_share_selected_adm_regions">
                          <span>{{adm_reg}}</span>
                      </label>
                    </li>
                    <li role="separator" class="divider"></li>
                    <li style="padding-left: 10px; padding-right: 10px;">
                      <span>Document Type</span>
                    </li>
                    <li v-for="doc_type in doc_types" style="padding-left: 10px; padding-right: 10px;">
                      <label class="dropdown-menu-item checkbox">
                        <input type="checkbox" :value="doc_type" v-model="topic_share_selected_doc_types">
                          <span>{{doc_type}}</span>
                      </label>
                    </li>
                    <li role="separator" class="divider"></li>
                    <li style="padding-left: 10px; padding-right: 10px;">
                      <span>Lending Instrument</span>
                    </li>
                    <li v-for="lndinstr in lending_instruments" style="padding-left: 10px; padding-right: 10px;">
                      <label class="dropdown-menu-item checkbox">
                        <input type="checkbox" :value="lndinstr" v-model="topic_share_selected_lending_instruments">
                          <span>{{lndinstr}}</span>
                      </label>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!topic_share_active && !topic_map_active" class="container" style="margin-top:50px;">
        <div v-show="!is_searching && !topic_share_active && !topic_map_active" class="documents-container">
          <div v-if="documents.length<1 && errors.length<1" class="no-documents-found">No matching results were found!</div>

          <div v-if="errors.length>0" class="error">
            <!-- <h3>Search Error:</h3> -->
            <!-- <pre>{{errors}}</pre> -->
            <div style="margin: 20px;">
              <div class="alert alert-warning">
                  <h4 class="alert-heading"><i class="fa fa-warning"></i> Sorry!</h4>
                  <p>We encountered some technical difficulties while processing your request. We know it's frustrating but rest assured we'll fix the problem ASAP!</p>
                  <hr>
                  <p class="mb-0">In the meantime, you can try other queries or change some parameters.</p>
              </div>
            </div>
          </div>

          <div v-if="documents.length>0" class="documents-found">
            <div>Top {{documents.length}} of 200,000+</div>
            <div class="row">
              <div class="col-md-9">

                <!-- start documents -->
                <div id="documents">
                  <div class="row document-row" v-for="document in documents">
                    <div class="col-md-1">
                      <span>
                        <i class="far fa-file-alt document-icon"></i>
                      </span>
                    </div>
                    <div class="col-md-11">
                      <h5><a :href="document.metadata.url_pdf" target="_blank">{{ document.metadata.title }}</a> <span class="badge badge-pill badge-info" v-if="document.metadata.year">{{document.metadata.year}}</span></h5>
                      <div>
                        <span class="badge badge-pill badge-secondary">ID: {{document.id}}</span>
                        <span>Rank: {{document.rank}}</span>,
                        <span>Score: {{document.score}}</span>
                      </div>
                      <div class="document-actions">
                        <a v-on:click="setCurrentDocument(document)" style="margin-right:15px;" xclass="btn btn-outline-primary btn-sm" data-toggle="collapse" :href="'#metadata-'+document.id" role="button" aria-expanded="false" aria-controls="collapse">
                          <i class="fas fa-stream"></i> Metadata
                        </a>

                        <a v-on:click="findRelatedDocuments(document)" :href="'#similar-documents-'+document.id"
                        style="margin-right:15px;" xclass="btn btn-outline-primary btn-sm" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapse"

                        ><i class="fas fa-search"></i> Find similar documents</a>

                        <a v-show="(lda_model_id != '')" v-on:click="getDocTopics(document)" :href="'#lda-topic-'+document.id"
                        style="margin-right:15px;" xclass="btn btn-outline-primary btn-sm" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapse"

                        ><i class="fas fa-chart-bar"></i> LDA Topics</a>

                        <a v-on:click="setCurrentDocument(document)" :href="'#wb-topic-'+document.id"
                        style="margin-right:15px;" xclass="btn btn-outline-primary btn-sm" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapse"

                        ><i class="fas fa-list"></i> WB Topics</a>

                        <a v-on:click="setCurrentDocument(document)" :href="'#doc-countries-'+document.id"
                        style="margin-right:15px;" xclass="btn btn-outline-primary btn-sm" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapse"

                        ><i v-bind:class="{'fas fa-flag': Object.keys(document.metadata.countries).length > 0, 'fas fa-flag-checkered': Object.keys(document.metadata.countries).length == 0}"></i> Countries</a>

                      </div>

                      <div v-show="document.id == current_document_id" class="collapse" :id="'metadata-'+document.id">
                        <pre>{{document.metadata}}</pre>
                      </div>

                      <div v-show="document.id == reference_similar_document_id" class="collapse" :id="'similar-documents-'+document.id">

                        <div class="container">
                          <ul class="nav nav-tabs" :id="'sim-docs-nav-'+document.id" role="tablist">
                            <li class="nav-item">
                              <a class="nav-link active" :id="'word2vec-tab-'+document.id" data-toggle="tab" :href="'#word2vec-'+document.id" role="tab" :aria-controls="'word2vec-'+document.id" aria-selected="true">Word2Vec</a>
                            </li>
                            <li v-if="lda_model_id != ''" class="nav-item">
                              <a class="nav-link" :id="'lda-tab'+document.id" data-toggle="tab" :href="'#lda-'+document.id" role="tab" aria-controls="profile" aria-selected="false">LDA</a>
                            </li>
                          </ul>

                          <div class="tab-content" :id="'similarDocsContent-'+document.id">
                            <div class="tab-pane fade show active" :id="'word2vec-'+document.id" role="tabpanel" :aria-labelledby="'word2vec-tab-'+document.id" style="padding:20px;">
                              <!-- search -->
                              <ul>
                                <li v-for="sim_doc in reference_similar_document">
                                  <a :href="sim_doc.metadata.url_pdf" target='_blank'>{{sim_doc.metadata.title}}</a>
                                </li>
                              </ul>
                            </div>

                            <div v-if="lda_model_id != ''" class="tab-pane fade" :id="'lda-'+document.id" role="tabpanel" :aria-labelledby="'lda-tab-'+document.id" style="padding:20px;">
                              <ul>
                                <li v-for="sim_doc in reference_lda_similar_document">
                                  <a :href="sim_doc.metadata.url_pdf" target='_blank'>{{sim_doc.metadata.title}}</a>
                                </li>
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div v-show="document.id == reference_topic_words_id" class="collapse" :id="'lda-topic-'+document.id">
                        <ul>
                          <li v-for="tw in reference_topic_words">
                            Topic {{tw.topic}} ({{(tw.score * 100).toFixed(1)}}%):
                            <span style="margin-left: 2px;" v-for="w in tw.words.map(function(v) {return v.word})" class="badge badge-success">{{w}}</span>
                          </li>
                        </ul>
                      </div>

                      <div v-show="document.id == current_document_id" class="collapse" :id="'wb-topic-'+document.id">
                        <ul>
                          <li>
                            Topics:
                            <div v-for="w in document.metadata.topics_src.split(',')" style="margin-left: 5px;" class="badge badge-primary">{{w}}</div>
                          </li>
                          <li>
                            Subtopics:
                            <!--<div style="padding-left: 10px;"><span v-for="w in document.metadata.wb_subtopic_src.split(',')" class="badge badge-success">{{w}}</span></div>-->
                            <div v-for="w in document.metadata.wb_subtopic_src.split(',')" style="margin-left: 5px;" class="badge badge-info">{{w}}</div>
                          </li>
                        </ul>
                      </div>

                      <div v-show="document.id == current_document_id" class="collapse" :id="'doc-countries-'+document.id">
                        <ul v-if="Object.keys(document.metadata.countries).length > 0">
                          <!-- <li v-for="cdata in prepareAndSortCountries(document.metadata.countries)" class="flag" :id="cdata.country">{{cdata.country}}: {{cdata.count}} ({{cdata.proportion}}%)</li> -->
                          <li v-for="cdata in prepareAndSortCountries(document.metadata.countries)">{{cdata.country}}: {{cdata.count}} ({{cdata.proportion}}%)</li>
                        </ul>
                      </div>

                    </div>
                  </div>
                </div>
                <!-- end documents -->
              </div>

              <div v-if="words" class="col-md-3" style="border-left:1px solid gainsboro;">
                <h4>Similar words</h4>
                <!--<div class="word-row" v-for="word in words">
                  <div>{{word.word}}</div>
                  <div>{{word.rank}}, {{word.score}}</div>
                </div>-->
                <ul class="list-group list-group-flush" v-for="word in words">
                  <li class="list-group-item">{{word.word}}</li>
                </ul>
              </div>

              <div v-if="uploaded_doc_topics" class="col-md-3" style="border-left: 1px solid gainsboro;">
                <h4>Document topics</h4>
                <ul>
                  <li v-for="tw in uploaded_doc_topics">
                    Topic {{tw.topic}} ({{(tw.score * 100).toFixed(1)}}%): <span v-for="w in tw.words.map(function(v) {return v.word})" class="badge badge-success">{{w}}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="topic_share_active || topic_map_active" class="container" style="margin-top:10px;">

        <div v-show="topic_share_active" class="row">
          <div v-if="topic_words" class="col-md-2" style="border-left:1px solid gainsboro; margin-top:40px;">
            <h4>Topic words</h4>
            <!--<div class="word-row" v-for="word in words">
              <div>{{word.word}}</div>
              <div>{{word.rank}}, {{word.score}}</div>
            </div>-->
            <ul class="list-group list-group-flush" v-for="topic_word in topic_words">
              <li class="list-group-item">{{topic_word.word}}</li>
            </ul>
          </div>
          <!-- <div v-if="topic_share_active" class="col-md-10"> -->
          <div v-show="topic_shares && topic_share_plot_ready" class="col-md-10">
            <div id='myDiv' class="responsive-plot" style="height: 60vh;"></div>
          </div>
          <!-- </div> -->
        </div>

        <div v-show="topic_share_active && !topic_shares && !topic_share_searching">Start exploring topic shares by choosing the LDA model, set the topic of interest, and select the data partitions to compare.</div>

        <div v-show="topic_share_active && topic_share_searching"  class="loading-animation">
          <div class="d-flex justify-content-center">
            <div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status">
              <span class="sr-only">Analyzing topic shares...</span>
            </div>
          </div>
        </div>

        <div v-show="is_searching" class="loading-animation">
          <div class="d-flex justify-content-center">
            <div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status">
              <span class="sr-only">Searching, please wait...</span>
            </div>
          </div>
        </div>

        <div v-if="topic_map_active" class="documents-container">
          <div id='mapDiv' class="responsive-plot" style="height: 60vh;"></div>
        </div>
      </div>
    </div>

    <script>
      window.app = new Vue({
      el: "#app",
      data: {
        keywords: 'refugee',
        site_url:'http://wbes2474.worldbank.org/',
        api_url:'http://wbes2474:8910/api/related_docs',
        api_base_url:'http://wbes2474:8910/api/',
        is_searching:false,
        documents:[],
        words:[],
        errors:[],
        corpus_ids:[],
        corpus_id:'WB',
        word2vec_model_id:'ALL_50',
        lda_model_id:'ALL_50',
        partition:'ALL',
        word2vec_models:{},
        models:{},
        // state_ready:false,
        is_file_uploaded:false,
        current_document_id: null,
        reference_similar_document: [],
        reference_similar_document_id: null,
        reference_topic_words: [],
        reference_topic_words_id: null,
        reference_lda_similar_document: null,
        uploaded_doc_topics:null,
        reference_common_docs: null,
        topic_words:null,
        current_lda_model_topics:null,
        topic_shares:null,
        topic_share_active:false,
        topic_map_active:false,
        topic_id:0,
        topic_share_selected_adm_regions:[],
        topic_share_selected_doc_types:[],
        topic_share_selected_lending_instruments:[],
        topic_share_plot_ready:false,
        topic_share_searching:false,
        adm_regions: ['Africa', 'East Asia and Pacific', 'Europe and Central Asia', 'Latin America & Caribbean', 'Middle East and North Africa', 'Rest Of The World', 'South Asia', 'The world Region'],
        doc_types: ['Board Documents', 'Country Focus', 'Economic & Sector Work', 'Project Documents', 'Publications & Research'],
        lending_instruments: ['Development Policy Lending']
        },
        computed: {
          showAlert() {
          return this.name.length > 4 ? true : false;
        }
      },
      mounted: function () {
        this.getModels();

        this.setModel(this.word2vec_model_id, 'word2vec');
        this.setModel(this.lda_model_id, 'lda');  // Do this such that when we navigate to the Topic share explorer, the topics are already available.

        this.doSearch();
          // this.state_ready = false;
        },
        methods:{
          prepareAndSortCountries: function(arr) {
            // Set slice() to avoid to generate an infinite loop!
            var dlist = [];
            var total = Object.values(arr).reduce(
              function(a, b) {
                return a+b;
              }
            );
            var arr = Object.entries(arr);

            for (var i = 0; i<arr.length; i++) {
              dlist.push({
                "country": arr[i][0],
                "count": arr[i][1],
                "proportion": Math.round(100 * (100 * arr[i][1] / total))/100
              });
            }

            return dlist.slice().sort(function(a, b) {
              return  b.count - a.count;
            });
          },
          uploadFile: function(e){
            if (!this.isReady()) {
              return
            }

            window.x=this.$refs;
            file=this.$refs.file.files[0];
            this.is_file_uploaded = true
            // console.log(file);

            var data;

            data = new FormData();
            data.append('file', file);

            this.errors=[];
            let vm=this;
            this.uploaded_doc_topics = null
            this.is_searching=true;

            options={
              corpus_id: this.corpus_id,
              model_id: this.word2vec_model_id,
              topn: 10,
              clean_doc: true
            }

            $.ajax({
              url: this.api_url+'?'+$.param(options),
              data: data,
              processData: false,
              type: 'POST',
              method: 'POST',
              contentType:false,
              success: function (data) {
                vm.words = null;
                //vm.survey.id=data.survey.id;
                // vm.documents=data.docs;
                if("docs" in data){
                  vm.documents=data.docs;
                }
                // if ("words" in data){
                //     vm.words=data.words;
                // }
                console.log(data);
              },
              error: function(e){
                console.log(e);
                //vm.errors=e;
                vm.errors.push(e);
                vm.is_searching=false;
              }
            })
            .done(function() {
              vm.is_searching=false;
            })

            if (this.lda_model_id != '') {
              options={
                corpus_id: this.corpus_id,
                model_id: this.lda_model_id,
                topn_topics: 10,
                total_topic_score: 0.8,
                clean_doc: true
              }

              $.ajax({
                url: this.api_base_url+'lda_doc_topics'+'?'+$.param(options),
                data: data,
                processData: false,
                type: 'POST',
                method: 'POST',
                contentType:false,
                success: function (data) {
                  vm.words = null;
                  //vm.survey.id=data.survey.id;
                  // vm.documents=data.docs;
                  if("topics" in data){
                    vm.uploaded_doc_topics=data.topics;
                  }
                  // if ("words" in data){
                  //     vm.words=data.words;
                  // }
                  console.log(data);
                },
                error: function(e){
                  console.log(e);
                  //vm.errors=e;
                  vm.errors.push(e);
                  vm.is_searching=false;
                }
              })
              .done(function() {
                vm.is_searching=false;
              })
            }

            e.preventDefault();
          },
          setCurrentDocument: function(document) {
              this.current_document_id = document.id;
          },
          doSearch: function (e) {
            this.errors=[];

            if (!this.isReady()) {
              return
            }

            //'?raw_text=power+supply&corpus_id=IMF&model_id=ALL_50&topn=10&clean_doc=true'
            let vm=this;
            this.is_searching=true;
            this.documents=[];
            this.words=[];

            options={
              raw_text: this.keywords,
              corpus_id: this.corpus_id,
              model_id: this.word2vec_model_id,
              topn: 10,
              clean_doc: true
            }

            $.ajax
            ({
              type: "GET",
              url: this.api_url+'?'+$.param(options),
              //contentType: 'application/json',
              //dataType: 'json',
              //async: false,
              success: function (data) {
                //vm.survey.id=data.survey.id;
                if("docs" in data){
                  vm.documents=data.docs;
                }
                if ("words" in data){
                  vm.words=data.words;
                }
                console.log(data);
              },
              error: function(e){
                console.log(e);
                //vm.errors=e;
                vm.errors.push(e);
                vm.is_searching=false;
              }
            })
            .done(function() {
              vm.is_searching=false;
            })
          },
          findRelatedDocuments: function (document) {
            //'?raw_text=power+supply&corpus_id=IMF&model_id=ALL_50&topn=10&clean_doc=true'
            let vm=this;
            if (document.id != vm.reference_similar_document_id) {
              document_id = document.id;

              options={
                corpus_id: this.corpus_id,
                model_id: this.word2vec_model_id,
                topn: 10,
                clean_doc: true,
                id: document_id
              }
              this.errors=[];

              $.ajax
              ({
                type: "GET",
                url: this.api_base_url+'related_docs_by_id?'+$.param(options),
                success: function (data) {
                  if("docs" in data){
                    vm.reference_similar_document = data.docs;
                    vm.reference_similar_document_id = document_id
                  }
                  console.log(data);
                },
                error: function(e){
                  console.log(e);
                  vm.errors.push(e);
                  vm.is_searching=false;
                }
              })
              .done(function() {
                vm.is_searching=false;
              })
            }

            if ((document.id != vm.reference_lda_similar_document_id) && (this.lda_model_id != '')) {
              document_id = document.id;

              options={
                corpus_id: this.corpus_id,
                model_id: this.lda_model_id,
                topn: 10,
                clean_doc: true,
                id: document_id
              }
              this.errors=[];

              $.ajax
              ({
                type: "GET",
                url: this.api_base_url+'lda_related_docs_by_id?'+$.param(options),
                success: function (data) {
                  if("docs" in data){
                    vm.reference_lda_similar_document = data.docs;
                    vm.reference_lda_similar_document_id = document_id
                  }
                  console.log(data)
                },
                error: function(e){
                  console.log(e);
                  vm.errors.push(e);
                  vm.is_searching=false;
                }
              })
              .done(function() {
                vm.is_searching=false;
              })
            }
          },
          getDocTopics: function (document) {
            //'?raw_text=power+supply&corpus_id=IMF&model_id=ALL_50&topn=10&clean_doc=true'
            let vm=this;
            if (document.id == vm.reference_topic_words_id) {
              if (vm.reference_topic_words != null) {
                return
              }
            }
            document_id = document.id;

            options={
              corpus_id: this.corpus_id,
              model_id: this.lda_model_id,
              topn_topics: 10,
              total_topic_score:0.8,
              clean_doc: true,
              id: document_id
            }
            this.errors=[];

            $.ajax
            ({
              type: "GET",
              url: this.api_base_url+'lda_doc_topics_by_id?'+$.param(options),
              success: function (data) {
                if("topics" in data){
                  vm.reference_topic_words = data.topics;
                  vm.reference_topic_words_id = document_id;
                  // $(element_id).collapse('show');
                  // vm.documents=data.docs;
                }
                // if ("words" in data){
                //     vm.words=data.words;
                // }
                console.log(data);
              },
              error: function(e){
                console.log(e);
                //vm.errors=e;
                vm.errors.push(e);
                vm.is_searching=false;
              }
            })
            .done(function() {
              vm.is_searching=false;
            })
          },
          setCorpus: function (_corpus_id) {
            let vm=this;
            vm.corpus_id = _corpus_id;
            vm.word2vec_model_id = '';
            vm.lda_model_id = ''
            vm.partition = ''
          },
          setPartition: function (_partition) {
            let vm=this;
            vm.partition = _partition;
            vm.word2vec_model_id = '';
            vm.lda_model_id = '';
          },
          setModel: function (_model_id, model_name) {
            let vm=this;
            if (model_name == 'word2vec') {
              vm.word2vec_model_id = _model_id;
            } else if (model_name == 'lda') {
              // Assume that
              vm.lda_model_id = _model_id;

              options = {
                corpus_id: this.corpus_id,
                model_id: this.lda_model_id,
                topn_words: 10
              }

              $.ajax({
                type: "GET",
                url: this.api_base_url+'get_lda_model_topics'+'?'+$.param(options),
                success: function (data) {
                  console.log(data);
                  vm.current_lda_model_topics = data;
                }
              })

            } else {
              return
            }
            // vm.state_ready = true;
          },
          isReady: function () {
            // Depend only on word2vec_model_id
            model_ready = (this.word2vec_model_id != '') && (this.corpus_id != '');
            return model_ready;
            // if (!(this.keywords.length > 0 || this.is_file_uploaded) || !model_ready) {
            //     return false;
            // } else {
            //     return true;
            // }
          },
          getModels: function () {
            let vm=this;
            $.ajax
            ({
              type: "GET",
              url: this.api_base_url+'get_models',
              success: function (data) {
                console.log(data);
                vm.models = data;
                if ("WORD2VEC" in data) {
                  vm.word2vec_models = data.WORD2VEC;
                  // Assume that the word2vec contains all corpus
                  if (vm.corpus_ids.length == 0) {
                    vm.corpus_ids = $.map(data.WORD2VEC, function(v, k) {
                      return k;
                    })
                  }
                }
              }
            })
          },
          plotStack: function(topic_shares) {
            this.topic_share_plot_ready = false;

            keys = Object.keys(topic_shares);
            traces = [];

            ph = 200.0
            ps = 20.0

            height = (ph * keys.length) + (ps * (keys.length - 1))
            div_dt = ps / height;
            panel_dt = ph / height;

            var layout = {
              title: "Topic share per document group",
              xaxis: {domain: [0, 1], title: "Year"},
              // yaxis: {domain: [0, 0.325]},
              // yaxis2: {domain: [0.35, 0.675]},
              // yaxis3: {domain: [0.7, 1]},
              // yaxis4: {domain: [0.85, 1]},
              height: height,
              // xaxis4: {
              //   domain: [0.55, 1],
              //   anchor: 'y4'
              // },
              // xaxis2: {domain: [0.55, 1]},
              // yaxis3: {domain: [0.55, 1]},
              // yaxis4: {
              //   domain: [0.55, 1],
              //   anchor: 'x4'
              // }
              autosize: true
            };

            Plotly.newPlot('myDiv', traces, layout);

            ix = 1;
            yd_start = 0;
            yd_end = yd_start + panel_dt;
            max_y = 0

            for (name in topic_shares) {
              y = topic_shares[name].map(function (x) {return x.topic_share}),
              y_max = Math.max.apply(null, y);

              if (y_max > max_y) {
                max_y = y_max;
              }

              tr = {
                x: topic_shares[name].map(function (x) { return x.year}),
                y: y,
                name: name,
                type: 'bar'
              }
              if (ix > 1) {
                tr.xaxis = 'x';
                tr.yaxis = 'y' + ix;
              }

              traces.push(tr)
              ix += 1;
            }

            for (ix=1; ix<=keys.length; ix++) {
              if (ix > 1) {
                layout['yaxis' + ix] = {domain: [yd_start, yd_end], range: [0, max_y]};
              } else {
                layout.yaxis = {domain: [yd_start, yd_end], range: [0, max_y]};
              }

              yd_start = yd_end + div_dt;
              yd_end = yd_start + panel_dt;
            }

            layout.legend = {orientation: 'h', x: 0, y: 1};

            Plotly.newPlot('myDiv', traces, layout);

            // myPlot = document.getElementById('myDiv');
            // myPlot.on('plotly_afterplot', function() {
            //   this.topic_share_plot_ready = true;
            // });

            // Make the plotly responsive
            // https://gist.github.com/aerispaha/63bb83208e6728188a4ee701d2b25ad5
            this.makeResponsive();

            this.topic_share_plot_ready = true;
            return true;
          },
          makeResponsive: function () {
            var d3 = Plotly.d3;
            var WIDTH_IN_PERCENT_OF_PARENT = 100,
                HEIGHT_IN_PERCENT_OF_PARENT = 100;

            var gd3 = d3.selectAll(".responsive-plot")
                .style({
                  width: WIDTH_IN_PERCENT_OF_PARENT + '%',
                  'margin-left': (100 - WIDTH_IN_PERCENT_OF_PARENT) / 2 + '%',

                  height: HEIGHT_IN_PERCENT_OF_PARENT + 'vh',
                  'margin-top': (100 - HEIGHT_IN_PERCENT_OF_PARENT) / 2 + 'vh'
                });

            var nodes_to_resize = gd3[0]; //not sure why but the goods are within a nested array

            // Important to run this explicitly here to fix some weird resizing behavior.
            (function() {
              for (var i = 0; i < nodes_to_resize.length; i++) {
                Plotly.Plots.resize(nodes_to_resize[i]);
              }
            })();

            window.onresize = function() {
              for (var i = 0; i < nodes_to_resize.length; i++) {
                Plotly.Plots.resize(nodes_to_resize[i]);
              }
            };
          },
          topicShareActiveToggle: function(topic_share_active, topic_map_active) {
            if (topic_share_active == this.topic_share_active) {
              return
            } else {
              this.topic_share_active = topic_share_active;
              this.topicMapActiveToggle(topic_map_active, this.topic_share_active);
            }
          },
          topicMapActiveToggle: function(topic_map_active, topic_share_active) {
            if (topic_map_active == this.topic_map_active) {
              return
            } else {
              this.topic_map_active = topic_map_active;
              this.topicShareActiveToggle(topic_share_active, this.topic_map_active);
            }
          },
          togglePanels: function (topic_map_active, topic_share_active) {
            this.topicShareActiveToggle(topic_share_active, topic_map_active);
            this.topicMapActiveToggle(topic_map_active, topic_share_active);
          },
          findTopicShare: function(topic_id, model_id, corpus_id) {
            let vm=this;
            this.topic_share_searching = true;
            this.topic_share_plot_ready = false;

            options={
              corpus_id: this.corpus_id,
              model_id: this.lda_model_id,
              topic_id: this.topic_id,
              year_start: 1960,
              adm_regions: this.topic_share_selected_adm_regions,
              major_doc_types: this.topic_share_selected_doc_types,
              lending_instruments: this.topic_share_selected_lending_instruments
            }

            $.ajax({
              url: this.api_base_url+'lda_compare_partition_topic_share'+'?'+$.param(options, true),
              // data: options,
              processData: false,
              type: 'POST',
              method: 'POST',
              contentType:false,
              success: function (data) {
                if("topic_shares" in data){
                  vm.topic_shares=data.topic_shares;
                }
                if ("topic_words" in data) {
                  vm.topic_words = data.topic_words
                }
                console.log(data);
              },
              error: function(e){
                console.log(e);
                vm.errors.push(e);
                vm.topic_share_searching=false;
              }
            })
            .done(function() {
              vm.topic_share_searching=false;
              vm.plotStack(vm.topic_shares);
            })
          },
          findTopicMap: function(topic_id, model_id, corpus_id) {
            let vm=this;
            drawMap('/nlp/country_popularity.csv', 'mapDiv');
            // this.makeResponsive();
          },
        }
      })
    </script>
  </body>
</html>

<!-- <div class="container">
  <div class="row">
    <div class="col-lg-12">
      <div class="button-group">
        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">Data Partitions</button>
        <ul class="dropdown-menu">
          <li>Admin Region</li>
          <li v-for="adm_reg in adm_regions" :value="adm_reg" v-model="topic_share_selected_adm_regions">{{adm_reg}}</li>
          <li role="separator" class="divider"></li>
          <li>Document Type</li>
          <li v-for="doc_type in doc_types" :value="doc_type" v-model="topic_share_selected_doc_types">{{doc_type}}</li>
          <li role="separator" class="divider"></li>
          <li>Lending Instruments</li>
          <li v-for="lndinstr in lending_instruments" :value="lndinstr" v-model="topic_share_selected_lending_instruments">{{lndinstr}}</li>
        </ul>
      </div>
    </div>
  </div>
</div>
 -->
<!--

model_map = {
    'AFR': 'Africa',
    'EAP': 'East Asia and Pacific',
    'ECA': 'Europe and Central Asia',

    'LAC': 'Latin America & Caribbean',
    'MENA': 'Middle East and North Africa',
    'RoW': 'Rest Of The World',
    'SAR': 'South Asia',
    'WLD': 'The world Region',

    'BD': 'Board Documents',
    'CF': 'Country Focus',
    'ESW': 'Economic & Sector Work',
    'PD': 'Project Documents',
    'PR': 'Publications & Research',
}
 -->

<!--
url = 'http://localhost:8910/api/related_docs_by_id'
url = 'http://localhost:8910/api/related_words'

url = 'http://localhost:8910/api/get_models'
data = requests.post(
  url,
  json = {
    'model_id': 'ALL_50',
    'corpus_id': 'IMF',
    'use_ngram':False,
    'topn': 10,
    'clean_doc': True,
    'id': 'imf_0014531c0ebcc88b9249f54029b7b78c0ef9f8f8'
#         'raw_text': 'purchasing power parity',
  },


url = 'http://localhost:8910/api/get_models'
data = requests.post(
  url, headers=headers
)
print(data.json())

url = 'http://localhost:8910/api/related_words'
data = requests.post(
  url, json={'raw_text': 'big data'},
  headers=headers
)
print(data.json())
-->
