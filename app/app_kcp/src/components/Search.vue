<template>
  <div>
    <header class="blog-header wbg-internal-header">
      <div class="container">
        <div class="col-12 mb-2">
          <div id="breadcrumbs">
            <router-link to="/">Home</router-link>
            <span class="wbg-breadcrumb-separator">/</span>
            <router-link to="/search">Search</router-link>
          </div>
        </div>
        <div class="col-12">
          <i class="fas fa-search fa-2x" aria-hidden="true"></i>
          <h1>Search</h1>
          <p></p>
        </div>
      </div>
    </header>

    <div class="container">
      <div class="row">
        <div class="row justify-content-center mb-4">
          <div class="col-12 col-md-8">
            <div class="input-group mb-3 mt-3" style="display: flex">
              <!-- <input
                    v-model="query"
                    type="text"
                    class="form-control wbg-search-text pl-4"
                    placeholder="Enter your keywords..."
                    aria-label="Field for search"
                    aria-describedby="basic-addon2"
                    v-on:keyup.enter="sendSearch()"
                  /> -->
              <!-- <div class="input-group-append">
                    <button
                      @click="sendSearch()"
                      class="btn btn-primary wbg-search-button pr-4 pl-4"
                      type="button"
                    >
                      Search
                    </button>
                  </div> -->
            </div>
          </div>
          <div class="col-12 col-md-8 text-center">
            <div class="form-check form-check-inline">
              <!-- <input
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio1"
                value="keyword"
                checked=""
                v-model="search_type"
                @change="resetFrom"
              />
              <label class="form-check-label" for="inlineRadio1"
                >Keyword search</label
              > -->
            </div>
            <div class="form-check form-check-inline">
              <!-- <input
                class="form-check-input"
                type="radio"
                name="inlineRadioOptions"
                id="inlineRadio2"
                value="semantic"
                v-model="search_type"
                @change="resetFrom"
              />
              <label class="form-check-label" for="inlineRadio2"
                >Semantic search</label
              > -->
            </div>
          </div>
        </div>

        <div class="col-12 col-md-12 mb-2">
          <div class="row justify-content-center">
            <div class="col-12 col-md-9 col-lg-8">
              <div
                class="input-group wbg-input-group mb-3 mt-3"
                style="display: flex"
              >
                <input
                  v-model="query"
                  type="text"
                  class="form-control wbg-search-text pl-4"
                  placeholder="Enter your keywords..."
                  aria-label="Field for search"
                  aria-describedby="basic-addon2"
                  v-on:keyup.enter="sendSearch()"
                />
                <!-- <input
                  type="text"
                  class="form-control wbg-search-text pl-4"
                  placeholder="Enter your keywords..."
                  aria-label="Field for search"
                  aria-describedby="basic-addon2"
                /> -->
                <div
                  id="submit_file"
                  data-toggle="tooltip"
                  data-placement="bottom"
                  title="Upload a PDF or TXT document to search"
                >
                  <div class="file-input">
                    <input
                      type="file"
                      name="file-input"
                      id="file-input"
                      class="file-input__input"
                      data-toggle="tooltip"
                      data-placement="bottom"
                      title="Upload a PDF or TXT document to search"
                    />
                    <label class="file-input__label" for="file-input"
                      ><i class="fas fa-file-upload fa-lg"></i
                    ></label>
                  </div>
                </div>
                <div class="input-group-append">
                  <button
                    @click="sendSearch()"
                    class="btn btn-primary wbg-search-button pr-4 pl-4"
                    type="button"
                  >
                    Search
                  </button>
                </div>
                <!-- <div class="input-group-append">
                  <button
                    class="btn btn-primary wbg-search-button pr-4 pl-4"
                    type="button"
                  >
                    Search
                  </button>
                </div> -->
              </div>
            </div>
            <div class="col-12 col-md-12 text-center">
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio1"
                  value="keyword"
                  checked
                  v-model="search_type"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio1"
                  >Keyword search</label
                >
                <!-- <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio1"
                  value="option1"
                  checked
                />
                <label class="form-check-label" for="inlineRadio1"
                  >Keyword search</label
                > -->
              </div>
              <div class="form-check form-check-inline">
                <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio2"
                  value="semantic"
                  v-model="search_type"
                  @change="resetFrom"
                />
                <label class="form-check-label" for="inlineRadio2"
                  >Semantic search</label
                >
                <!-- <input
                  class="form-check-input"
                  type="radio"
                  name="inlineRadioOptions"
                  id="inlineRadio2"
                  value="option2"
                />
                <label class="form-check-label" for="inlineRadio2"
                  >Semantic search</label
                > -->
              </div>
            </div>
            <div class="col-12 text-center mt-3">
              <small
                >You can also try
                <a href="#">filtering by topic composition</a></small
              >
            </div>
          </div>
          <hr />
        </div>
        <aside class="col-sm-3 blog-sidebar">
          <div>
            <div
              id="filter-by-access"
              class="sidebar-filter wb-ihsn-sidebar-filter filter-by-year filter-box"
            >
              <h6 class="togglable">
                <i class="fa fa-search pr-2"></i>Filter by Year
              </h6>
              <div class="sidebar-filter-entries">
                <input type="hidden" />
                <p class="mt-3 mb-2">Show studies conducted between</p>
                <div class="form-group">
                  <select name="from" id="from" class="form-control">
                    <option value="2020">2020</option>
                    <option value="2019">2019</option>
                    <option value="2018">2018</option>
                    <option value="2017">2017</option>
                    <option value="2016">2016</option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
                    <option value="2012">2012</option>
                    <option value="2011">2011</option>
                    <option value="2010">2010</option>
                    <option value="2009">2009</option>
                    <option value="2008">2008</option>
                    <option value="2007">2007</option>
                    <option value="2006">2006</option>
                    <option value="2005">2005</option>
                    <option value="2004">2004</option>
                    <option value="2003">2003</option>
                    <option value="2002">2002</option>
                    <option value="2001">2001</option>
                    <option value="2000">2000</option>
                    <option value="1999">1999</option>
                    <option value="1998">1998</option>
                    <option value="1997">1997</option>
                    <option value="1996">1996</option>
                    <option value="1995">1995</option>
                    <option value="1994">1994</option>
                    <option value="1993">1993</option>
                    <option value="1992">1992</option>
                    <option value="1991">1991</option>
                    <option value="1990">1990</option>
                    <option value="1989">1989</option>
                    <option value="1988">1988</option>
                    <option value="1987">1987</option>
                    <option value="1986">1986</option>
                    <option value="1985">1985</option>
                    <option value="1984">1984</option>
                    <option value="1983">1983</option>
                    <option value="1982">1982</option>
                    <option value="1981">1981</option>
                    <option value="1980">1980</option>
                    <option value="1979">1979</option>
                    <option value="1978">1978</option>
                    <option value="1977">1977</option>
                    <option value="1976">1976</option>
                    <option value="1975">1975</option>
                    <option value="1974">1974</option>
                    <option value="1973">1973</option>
                    <option value="1972">1972</option>
                    <option value="1971">1971</option>
                    <option value="1970">1970</option>
                    <option value="1969">1969</option>
                    <option value="1968">1968</option>
                    <option value="1967">1967</option>
                    <option value="1966">1966</option>
                    <option value="1965">1965</option>
                    <option value="1964">1964</option>
                    <option value="1963">1963</option>
                    <option value="1962">1962</option>
                    <option value="1961">1961</option>
                    <option value="1960">1960</option>
                    <option value="1959">1959</option>
                    <option value="1958">1958</option>
                    <option value="1957">1957</option>
                    <option value="1956">1956</option>
                    <option value="1955">1955</option>
                    <option value="1954">1954</option>
                    <option value="1953">1953</option>
                    <option value="1952">1952</option>
                    <option value="1951">1951</option>
                    <option value="1950">1950</option>
                    <option value="1949">1949</option>
                    <option value="1948">1948</option>
                    <option value="1947">1947</option>
                    <option value="1946">1946</option>
                    <option value="1945">1945</option>
                    <option value="1944">1944</option>
                    <option value="1943">1943</option>
                    <option value="1942">1942</option>
                    <option value="1941">1941</option>
                    <option value="1940">1940</option>
                    <option value="1939">1939</option>
                    <option value="1938">1938</option>
                    <option value="1937">1937</option>
                    <option value="1936">1936</option>
                    <option value="1935">1935</option>
                    <option value="1934">1934</option>
                    <option value="1933">1933</option>
                    <option value="1932">1932</option>
                    <option value="1931">1931</option>
                    <option value="1930">1930</option>
                    <option value="1929">1929</option>
                    <option value="1928">1928</option>
                    <option value="1927">1927</option>
                    <option value="1926">1926</option>
                    <option value="1925">1925</option>
                    <option value="1924">1924</option>
                    <option value="1923">1923</option>
                    <option value="1922">1922</option>
                    <option value="1921">1921</option>
                    <option value="1920">1920</option>
                    <option value="1919">1919</option>
                    <option value="1918">1918</option>
                    <option value="1917">1917</option>
                    <option value="1916">1916</option>
                    <option value="1915">1915</option>
                    <option value="1914">1914</option>
                    <option value="1913">1913</option>
                    <option value="1912">1912</option>
                    <option value="1911">1911</option>
                    <option value="1910">1910</option>
                    <option value="1909">1909</option>
                    <option value="1908">1908</option>
                    <option value="1907">1907</option>
                    <option value="1906">1906</option>
                    <option value="1905">1905</option>
                    <option value="1904">1904</option>
                    <option value="1903">1903</option>
                    <option value="1902">1902</option>
                    <option value="1901">1901</option>
                    <option value="1900">1900</option>
                    <option value="1899">1899</option>
                    <option value="1898">1898</option>
                    <option value="1897">1897</option>
                    <option value="1896">1896</option>
                    <option value="1895">1895</option>
                    <option value="1894">1894</option>
                    <option value="1893">1893</option>
                    <option value="1892">1892</option>
                    <option value="1891">1891</option>
                    <option value="1890" selected>1890</option>
                  </select>
                </div>
                <p class="mt-3 mb-2">and</p>
                <div class="form-group">
                  <select name="to" id="to" class="form-control">
                    <option value="2020">2020</option>
                    <option value="2019">2019</option>
                    <option value="2018">2018</option>
                    <option value="2017">2017</option>
                    <option value="2016">2016</option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
                    <option value="2012">2012</option>
                    <option value="2011">2011</option>
                    <option value="2010">2010</option>
                    <option value="2009">2009</option>
                    <option value="2008">2008</option>
                    <option value="2007">2007</option>
                    <option value="2006">2006</option>
                    <option value="2005">2005</option>
                    <option value="2004">2004</option>
                    <option value="2003">2003</option>
                    <option value="2002">2002</option>
                    <option value="2001">2001</option>
                    <option value="2000">2000</option>
                    <option value="1999">1999</option>
                    <option value="1998">1998</option>
                    <option value="1997">1997</option>
                    <option value="1996">1996</option>
                    <option value="1995">1995</option>
                    <option value="1994">1994</option>
                    <option value="1993">1993</option>
                    <option value="1992">1992</option>
                    <option value="1991">1991</option>
                    <option value="1990">1990</option>
                    <option value="1989">1989</option>
                    <option value="1988">1988</option>
                    <option value="1987">1987</option>
                    <option value="1986">1986</option>
                    <option value="1985">1985</option>
                    <option value="1984">1984</option>
                    <option value="1983">1983</option>
                    <option value="1982">1982</option>
                    <option value="1981">1981</option>
                    <option value="1980">1980</option>
                    <option value="1979">1979</option>
                    <option value="1978">1978</option>
                    <option value="1977">1977</option>
                    <option value="1976">1976</option>
                    <option value="1975">1975</option>
                    <option value="1974">1974</option>
                    <option value="1973">1973</option>
                    <option value="1972">1972</option>
                    <option value="1971">1971</option>
                    <option value="1970">1970</option>
                    <option value="1969">1969</option>
                    <option value="1968">1968</option>
                    <option value="1967">1967</option>
                    <option value="1966">1966</option>
                    <option value="1965">1965</option>
                    <option value="1964">1964</option>
                    <option value="1963">1963</option>
                    <option value="1962">1962</option>
                    <option value="1961">1961</option>
                    <option value="1960">1960</option>
                    <option value="1959">1959</option>
                    <option value="1958">1958</option>
                    <option value="1957">1957</option>
                    <option value="1956">1956</option>
                    <option value="1955">1955</option>
                    <option value="1954">1954</option>
                    <option value="1953">1953</option>
                    <option value="1952">1952</option>
                    <option value="1951">1951</option>
                    <option value="1950">1950</option>
                    <option value="1949">1949</option>
                    <option value="1948">1948</option>
                    <option value="1947">1947</option>
                    <option value="1946">1946</option>
                    <option value="1945">1945</option>
                    <option value="1944">1944</option>
                    <option value="1943">1943</option>
                    <option value="1942">1942</option>
                    <option value="1941">1941</option>
                    <option value="1940">1940</option>
                    <option value="1939">1939</option>
                    <option value="1938">1938</option>
                    <option value="1937">1937</option>
                    <option value="1936">1936</option>
                    <option value="1935">1935</option>
                    <option value="1934">1934</option>
                    <option value="1933">1933</option>
                    <option value="1932">1932</option>
                    <option value="1931">1931</option>
                    <option value="1930">1930</option>
                    <option value="1929">1929</option>
                    <option value="1928">1928</option>
                    <option value="1927">1927</option>
                    <option value="1926">1926</option>
                    <option value="1925">1925</option>
                    <option value="1924">1924</option>
                    <option value="1923">1923</option>
                    <option value="1922">1922</option>
                    <option value="1921">1921</option>
                    <option value="1920">1920</option>
                    <option value="1919">1919</option>
                    <option value="1918">1918</option>
                    <option value="1917">1917</option>
                    <option value="1916">1916</option>
                    <option value="1915">1915</option>
                    <option value="1914">1914</option>
                    <option value="1913">1913</option>
                    <option value="1912">1912</option>
                    <option value="1911">1911</option>
                    <option value="1910">1910</option>
                    <option value="1909">1909</option>
                    <option value="1908">1908</option>
                    <option value="1907">1907</option>
                    <option value="1906">1906</option>
                    <option value="1905">1905</option>
                    <option value="1904">1904</option>
                    <option value="1903">1903</option>
                    <option value="1902">1902</option>
                    <option value="1901">1901</option>
                    <option value="1900">1900</option>
                    <option value="1899">1899</option>
                    <option value="1898">1898</option>
                    <option value="1897">1897</option>
                    <option value="1896">1896</option>
                    <option value="1895">1895</option>
                    <option value="1894">1894</option>
                    <option value="1893">1893</option>
                    <option value="1892">1892</option>
                    <option value="1891">1891</option>
                    <option value="1890">1890</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <header></header>

            <div class="nada-pagination" v-show="hits.length > 0">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-md-3 col-lg-4 mb-3 mb-md-0 small">
                  Showing <b>{{ start }}-{{ end }}</b> of
                  <b>{{ total.message }}</b> studies
                </div>
                <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary btn-sm dropdown-toggle wbg-button"
                      type="button"
                      id="dropdownMenuButton"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Sort by
                    </button>
                    <div
                      class="dropdown-menu"
                      aria-labelledby="dropdownMenuButton"
                    >
                      <a class="dropdown-item" href="#">Relevance</a>
                      <a class="dropdown-item" href="#">Release date</a>
                      <a class="dropdown-item" href="#">Trending (past day)</a>
                      <a class="dropdown-item" href="#">Trending (past week)</a>
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm wbg-button ml-2"
                  >
                    <i class="fas fa-chart-bar fa-lg mr-1"></i>Show statistics
                  </button>
                  <a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-print"></i></a
                  ><a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-file-excel-o"></i
                  ></a>
                </div>
              </div>
              <!-- <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary btn-sm dropdown-toggle wbg-button"
                      type="button"
                      id="dropdownMenuButton"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Sort by
                    </button>
                    <div
                      class="dropdown-menu"
                      aria-labelledby="dropdownMenuButton"
                    >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Relevance</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Release date</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Trending (past day)</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Trending (past week)</a
                      >
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm wbg-button ml-2"
                  >
                    <i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Show statistics
                  </button>
                  <a
                    target="_blank"
                    href="https://mtt-wb21h.netlify.app/search/#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-print" aria-hidden="true"></i></a
                  ><a
                    target="_blank"
                    href="https://mtt-wb21h.netlify.app/search/#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-file-excel-o" aria-hidden="true"></i
                  ></a>
                </div>
              </div> -->
              <!-- </div> -->

              <!--
            <div class="nada-pagination">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-md-3 col-lg-4 mb-3 mb-md-0 small">
                  Showing <b>1-15</b> of <b>3269</b> studies
                </div>
                <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary btn-sm dropdown-toggle wbg-button"
                      type="button"
                      id="dropdownMenuButton"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Sort by
                    </button>
                    <div
                      class="dropdown-menu"
                      aria-labelledby="dropdownMenuButton"
                    >
                      <a class="dropdown-item" href="#">Relevance</a>
                      <a class="dropdown-item" href="#">Release date</a>
                      <a class="dropdown-item" href="#">Trending (past day)</a>
                      <a class="dropdown-item" href="#">Trending (past week)</a>
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm wbg-button ml-2"
                  >
                    <i class="fas fa-chart-bar fa-lg mr-1"></i>Show statistics
                  </button>
                  <a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-print"></i></a
                  ><a
                    target="_blank"
                    href="#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-file-excel-o"></i
                  ></a>
                </div>
              </div> -->
            </div>
            <div class="document-row" data-url="#" title="View study">
              <div class="row">
                <div class="col-3 col-lg-3">
                  <img
                    src="/static/files/doc_thumb.png"
                    title="document thumbnail"
                    alt="document thumbnail"
                  />
                </div>
                <div class="col-9 col-lg-9">
                  <span class="badge badge-primary wbg-badge">DOCUMENT</span>
                  <h5 class="title">
                    <a
                      href="#"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a href="#"
                        >MEASURE DHS: Demographic and Health Surveys</a
                      >
                    </div>
                  </div>
                  <div class="survey-stats">
                    <span>Created on: Mar 17, 2020</span>
                    <span>Last modified: Mar 17, 2020</span>
                    <span>Views: 3320</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="document-row" data-url="#" title="View study">
              <div class="row">
                <div class="col-3 col-lg-3">
                  <img
                    src="/static/files/doc_thumb.png"
                    title="document thumbnail"
                    alt="document thumbnail"
                  />
                </div>
                <div class="col-9 col-lg-9">
                  <span class="badge badge-primary wbg-badge">DOCUMENT</span>
                  <h5 class="title">
                    <a
                      href="#"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a href="#"
                        >MEASURE DHS: Demographic and Health Surveys</a
                      >
                    </div>
                  </div>
                  <div class="survey-stats">
                    <span>Created on: Mar 17, 2020</span>
                    <span>Last modified: Mar 17, 2020</span>
                    <span>Views: 3320</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="document-row" data-url="#" title="View study">
              <div class="row">
                <div class="col-3 col-lg-3">
                  <img
                    src="/static/files/doc_thumb.png"
                    title="document thumbnail"
                    alt="document thumbnail"
                  />
                </div>
                <div class="col-9 col-lg-9">
                  <span class="badge badge-primary wbg-badge">DOCUMENT</span>
                  <h5 class="title">
                    <a
                      href="#"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a href="#"
                        >MEASURE DHS: Demographic and Health Surveys</a
                      >
                    </div>
                  </div>
                  <div class="survey-stats">
                    <span>Created on: Mar 17, 2020</span>
                    <span>Last modified: Mar 17, 2020</span>
                    <span>Views: 3320</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="document-row" data-url="#" title="View study">
              <div class="row">
                <div class="col-3 col-lg-3">
                  <img
                    src="/static/files/doc_thumb.png"
                    title="document thumbnail"
                    alt="document thumbnail"
                  />
                </div>
                <div class="col-9 col-lg-9">
                  <span class="badge badge-primary wbg-badge">DOCUMENT</span>
                  <h5 class="title">
                    <a
                      href="#"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a href="#"
                        >MEASURE DHS: Demographic and Health Surveys</a
                      >
                    </div>
                  </div>
                  <div class="survey-stats">
                    <span>Created on: Mar 17, 2020</span>
                    <span>Last modified: Mar 17, 2020</span>
                    <span>Views: 3320</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="document-row" data-url="#" title="View study">
              <div class="row">
                <div class="col-3 col-lg-3">
                  <img
                    src="/static/files/doc_thumb.png"
                    title="document thumbnail"
                    alt="document thumbnail"
                  />
                </div>
                <div class="col-9 col-lg-9">
                  <span class="badge badge-primary wbg-badge">DOCUMENT</span>
                  <h5 class="title">
                    <a
                      href="#"
                      title="Service Provision Assessment Survey 2018-2019"
                      >Service Provision Assessment Survey 2018-2019</a
                    >
                  </h5>
                  <div class="study-country">Afghanistan, 2018-2019</div>
                  <div class="sub-title">
                    <div>
                      <span class="study-by">Ministry of Public Health</span>
                    </div>
                    <div class="owner-collection">
                      Collection:
                      <a href="#"
                        >MEASURE DHS: Demographic and Health Surveys</a
                      >
                    </div>
                  </div>
                  <div class="survey-stats">
                    <span>Created on: Mar 17, 2020</span>
                    <span>Last modified: Mar 17, 2020</span>
                    <span>Views: 3320</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="nada-pagination mt-5">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-lg-6 mb-3 small">
                  <div
                    id="items-per-page"
                    class="items-per-page light switch-page-size"
                  >
                    <small
                      >Results per page
                      <span class="wbg-pagination-btn active">15</span>
                      <span class="wbg-pagination-btn">30</span>
                      <span class="wbg-pagination-btn">50</span>
                      <span class="wbg-pagination-btn">100</span></small
                    >
                  </div>
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-lg-end">
                  <nav aria-label="Page navigation">
                    <ul
                      class="pagination pagination-md wbg-pagination-ul small"
                    >
                      <li class="page-item">
                        <a href="#" class="page-link active" data-page="1">1</a>
                      </li>
                      <li class="page-item">
                        <a href="#" class="page-link" data-page="2">2</a>
                      </li>
                      <li class="page-item">
                        <a href="#" class="page-link" data-page="3">3</a>
                      </li>
                      <li class="page-item">
                        <a href="#" class="page-link" data-page="4">4</a>
                      </li>
                      <li class="page-item">
                        <a href="#" class="page-link" data-page="5">5</a>
                      </li>
                      <li class="page-item">
                        <a href="#" class="page-link" data-page="2">Next</a>
                      </li>
                      <li class="page-item">
                        <a
                          href="#"
                          class="page-link"
                          data-page="218"
                          title="Last"
                          >»</a
                        >
                      </li>
                    </ul>
                  </nav>
                </div>
              </div>
            </div>
            <hr />
            <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fsearch%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&url=%2fsearch%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fsearch%2f&text=Search"
                    title="Tweet this"
                    ><span class="fab fa-twitter fa-lg"></span
                  ></a>
                </nav>
              </section>
            </footer>
          </article>
        </div>
      </div>
    </div>

    <div class="container flowing">
      <div class="row">
        <aside class="col-sm-3 blog-sidebar" id="blog-sidebar">
          <div>
            <div
              id="filter-by-access"
              class="sidebar-filter wb-ihsn-sidebar-filter filter-by-year filter-box"
            >
              <h6 class="togglable">
                <i class="fa fa-search pr-2" aria-hidden="true"></i>Filter by
                Year
              </h6>
              <div class="sidebar-filter-entries">
                <input type="hidden" />
                <p class="mb-0">Show studies conducted between</p>
                <div class="form-group mb-0">
                  <input type="hidden" />
                  <select name="from" id="from" class="form-control">
                    <option value="2020">2020</option>
                    <option value="2019">2019</option>
                    <option value="2018">2018</option>
                    <option value="2017">2017</option>
                    <option value="2016">2016</option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
                    <option value="2012">2012</option>
                    <option value="2011">2011</option>
                    <option value="2010">2010</option>
                    <option value="2009">2009</option>
                    <option value="2008">2008</option>
                    <option value="2007">2007</option>
                    <option value="2006">2006</option>
                    <option value="2005">2005</option>
                    <option value="2004">2004</option>
                    <option value="2003">2003</option>
                    <option value="2002">2002</option>
                    <option value="2001">2001</option>
                    <option value="2000">2000</option>
                    <option value="1999">1999</option>
                    <option value="1998">1998</option>
                    <option value="1997">1997</option>
                    <option value="1996">1996</option>
                    <option value="1995">1995</option>
                    <option value="1994">1994</option>
                    <option value="1993">1993</option>
                    <option value="1992">1992</option>
                    <option value="1991">1991</option>
                    <option value="1990">1990</option>
                    <option value="1989">1989</option>
                    <option value="1988">1988</option>
                    <option value="1987">1987</option>
                    <option value="1986">1986</option>
                    <option value="1985">1985</option>
                    <option value="1984">1984</option>
                    <option value="1983">1983</option>
                    <option value="1982">1982</option>
                    <option value="1981">1981</option>
                    <option value="1980">1980</option>
                    <option value="1979">1979</option>
                    <option value="1978">1978</option>
                    <option value="1977">1977</option>
                    <option value="1976">1976</option>
                    <option value="1975">1975</option>
                    <option value="1974">1974</option>
                    <option value="1973">1973</option>
                    <option value="1972">1972</option>
                    <option value="1971">1971</option>
                    <option value="1970">1970</option>
                    <option value="1969">1969</option>
                    <option value="1968">1968</option>
                    <option value="1967">1967</option>
                    <option value="1966">1966</option>
                    <option value="1965">1965</option>
                    <option value="1964">1964</option>
                    <option value="1963">1963</option>
                    <option value="1962">1962</option>
                    <option value="1961">1961</option>
                    <option value="1960">1960</option>
                    <option value="1959">1959</option>
                    <option value="1958">1958</option>
                    <option value="1957">1957</option>
                    <option value="1956">1956</option>
                    <option value="1955">1955</option>
                    <option value="1954">1954</option>
                    <option value="1953">1953</option>
                    <option value="1952">1952</option>
                    <option value="1951">1951</option>
                    <option value="1950">1950</option>
                    <option value="1949">1949</option>
                    <option value="1948">1948</option>
                    <option value="1947">1947</option>
                    <option value="1946">1946</option>
                    <option value="1945">1945</option>
                    <option value="1944">1944</option>
                    <option value="1943">1943</option>
                    <option value="1942">1942</option>
                    <option value="1941">1941</option>
                    <option value="1940">1940</option>
                    <option value="1939">1939</option>
                    <option value="1938">1938</option>
                    <option value="1937">1937</option>
                    <option value="1936">1936</option>
                    <option value="1935">1935</option>
                    <option value="1934">1934</option>
                    <option value="1933">1933</option>
                    <option value="1932">1932</option>
                    <option value="1931">1931</option>
                    <option value="1930">1930</option>
                    <option value="1929">1929</option>
                    <option value="1928">1928</option>
                    <option value="1927">1927</option>
                    <option value="1926">1926</option>
                    <option value="1925">1925</option>
                    <option value="1924">1924</option>
                    <option value="1923">1923</option>
                    <option value="1922">1922</option>
                    <option value="1921">1921</option>
                    <option value="1920">1920</option>
                    <option value="1919">1919</option>
                    <option value="1918">1918</option>
                    <option value="1917">1917</option>
                    <option value="1916">1916</option>
                    <option value="1915">1915</option>
                    <option value="1914">1914</option>
                    <option value="1913">1913</option>
                    <option value="1912">1912</option>
                    <option value="1911">1911</option>
                    <option value="1910">1910</option>
                    <option value="1909">1909</option>
                    <option value="1908">1908</option>
                    <option value="1907">1907</option>
                    <option value="1906">1906</option>
                    <option value="1905">1905</option>
                    <option value="1904">1904</option>
                    <option value="1903">1903</option>
                    <option value="1902">1902</option>
                    <option value="1901">1901</option>
                    <option value="1900">1900</option>
                    <option value="1899">1899</option>
                    <option value="1898">1898</option>
                    <option value="1897">1897</option>
                    <option value="1896">1896</option>
                    <option value="1895">1895</option>
                    <option value="1894">1894</option>
                    <option value="1893">1893</option>
                    <option value="1892">1892</option>
                    <option value="1891">1891</option>
                    <option value="1890" selected="">1890</option>
                  </select>
                </div>
                <p class="mb-0">and</p>
                <div class="form-group">
                  <select name="to" id="to" class="form-control">
                    <option value="2020">2020</option>
                    <option value="2019">2019</option>
                    <option value="2018">2018</option>
                    <option value="2017">2017</option>
                    <option value="2016">2016</option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    <option value="2013">2013</option>
                    <option value="2012">2012</option>
                    <option value="2011">2011</option>
                    <option value="2010">2010</option>
                    <option value="2009">2009</option>
                    <option value="2008">2008</option>
                    <option value="2007">2007</option>
                    <option value="2006">2006</option>
                    <option value="2005">2005</option>
                    <option value="2004">2004</option>
                    <option value="2003">2003</option>
                    <option value="2002">2002</option>
                    <option value="2001">2001</option>
                    <option value="2000">2000</option>
                    <option value="1999">1999</option>
                    <option value="1998">1998</option>
                    <option value="1997">1997</option>
                    <option value="1996">1996</option>
                    <option value="1995">1995</option>
                    <option value="1994">1994</option>
                    <option value="1993">1993</option>
                    <option value="1992">1992</option>
                    <option value="1991">1991</option>
                    <option value="1990">1990</option>
                    <option value="1989">1989</option>
                    <option value="1988">1988</option>
                    <option value="1987">1987</option>
                    <option value="1986">1986</option>
                    <option value="1985">1985</option>
                    <option value="1984">1984</option>
                    <option value="1983">1983</option>
                    <option value="1982">1982</option>
                    <option value="1981">1981</option>
                    <option value="1980">1980</option>
                    <option value="1979">1979</option>
                    <option value="1978">1978</option>
                    <option value="1977">1977</option>
                    <option value="1976">1976</option>
                    <option value="1975">1975</option>
                    <option value="1974">1974</option>
                    <option value="1973">1973</option>
                    <option value="1972">1972</option>
                    <option value="1971">1971</option>
                    <option value="1970">1970</option>
                    <option value="1969">1969</option>
                    <option value="1968">1968</option>
                    <option value="1967">1967</option>
                    <option value="1966">1966</option>
                    <option value="1965">1965</option>
                    <option value="1964">1964</option>
                    <option value="1963">1963</option>
                    <option value="1962">1962</option>
                    <option value="1961">1961</option>
                    <option value="1960">1960</option>
                    <option value="1959">1959</option>
                    <option value="1958">1958</option>
                    <option value="1957">1957</option>
                    <option value="1956">1956</option>
                    <option value="1955">1955</option>
                    <option value="1954">1954</option>
                    <option value="1953">1953</option>
                    <option value="1952">1952</option>
                    <option value="1951">1951</option>
                    <option value="1950">1950</option>
                    <option value="1949">1949</option>
                    <option value="1948">1948</option>
                    <option value="1947">1947</option>
                    <option value="1946">1946</option>
                    <option value="1945">1945</option>
                    <option value="1944">1944</option>
                    <option value="1943">1943</option>
                    <option value="1942">1942</option>
                    <option value="1941">1941</option>
                    <option value="1940">1940</option>
                    <option value="1939">1939</option>
                    <option value="1938">1938</option>
                    <option value="1937">1937</option>
                    <option value="1936">1936</option>
                    <option value="1935">1935</option>
                    <option value="1934">1934</option>
                    <option value="1933">1933</option>
                    <option value="1932">1932</option>
                    <option value="1931">1931</option>
                    <option value="1930">1930</option>
                    <option value="1929">1929</option>
                    <option value="1928">1928</option>
                    <option value="1927">1927</option>
                    <option value="1926">1926</option>
                    <option value="1925">1925</option>
                    <option value="1924">1924</option>
                    <option value="1923">1923</option>
                    <option value="1922">1922</option>
                    <option value="1921">1921</option>
                    <option value="1920">1920</option>
                    <option value="1919">1919</option>
                    <option value="1918">1918</option>
                    <option value="1917">1917</option>
                    <option value="1916">1916</option>
                    <option value="1915">1915</option>
                    <option value="1914">1914</option>
                    <option value="1913">1913</option>
                    <option value="1912">1912</option>
                    <option value="1911">1911</option>
                    <option value="1910">1910</option>
                    <option value="1909">1909</option>
                    <option value="1908">1908</option>
                    <option value="1907">1907</option>
                    <option value="1906">1906</option>
                    <option value="1905">1905</option>
                    <option value="1904">1904</option>
                    <option value="1903">1903</option>
                    <option value="1902">1902</option>
                    <option value="1901">1901</option>
                    <option value="1900">1900</option>
                    <option value="1899">1899</option>
                    <option value="1898">1898</option>
                    <option value="1897">1897</option>
                    <option value="1896">1896</option>
                    <option value="1895">1895</option>
                    <option value="1894">1894</option>
                    <option value="1893">1893</option>
                    <option value="1892">1892</option>
                    <option value="1891">1891</option>
                    <option value="1890">1890</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </aside>
        <div class="col-sm-9 blog-main">
          <article class="blog-post">
            <header></header>
            <div class="row justify-content-center mb-4">
              <!-- <div class="col-12 col-md-8">
                <div class="input-group mb-3 mt-3" style="display: flex">
                  <input
                    v-model="query"
                    type="text"
                    class="form-control wbg-search-text pl-4"
                    placeholder="Enter your keywords..."
                    aria-label="Field for search"
                    aria-describedby="basic-addon2"
                    v-on:keyup.enter="sendSearch()"
                  />
                  <div class="input-group-append">
                    <button
                      @click="sendSearch()"
                      class="btn btn-primary wbg-search-button pr-4 pl-4"
                      type="button"
                    >
                      Search
                    </button>
                  </div>
                </div>
              </div> -->
              <!-- <div class="col-12 col-md-8 text-center">
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="inlineRadioOptions"
                    id="inlineRadio1"
                    value="keyword"
                    checked=""
                    v-model="search_type"
                    @change="resetFrom"
                  />
                  <label class="form-check-label" for="inlineRadio1"
                    >Keyword search</label
                  >
                </div>
                <div class="form-check form-check-inline">
                  <input
                    class="form-check-input"
                    type="radio"
                    name="inlineRadioOptions"
                    id="inlineRadio2"
                    value="semantic"
                    v-model="search_type"
                    @change="resetFrom"
                  />
                  <label class="form-check-label" for="inlineRadio2"
                    >Semantic search</label
                  >
                </div>
              </div> -->
            </div>
            <hr />
            <div class="nada-pagination" v-show="hits.length > 0">
              <div
                class="row mt-4 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-md-3 col-lg-4 mb-2 mb-md-0 small">
                  Showing <b>{{ start }}-{{ end }}</b> of
                  <b>{{ total.message }}</b> studies
                </div>
                <div
                  class="filter-action-bar d-flex col-12 col-md-9 col-lg-8 justify-content-lg-end"
                >
                  <div class="dropdown">
                    <button
                      class="btn btn-outline-secondary btn-sm dropdown-toggle wbg-button"
                      type="button"
                      id="dropdownMenuButton"
                      data-toggle="dropdown"
                      aria-haspopup="true"
                      aria-expanded="false"
                    >
                      Sort by
                    </button>
                    <div
                      class="dropdown-menu"
                      aria-labelledby="dropdownMenuButton"
                    >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Relevance</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Release date</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Trending (past day)</a
                      >
                      <a
                        class="dropdown-item"
                        href="https://mtt-wb21h.netlify.app/search/#"
                        >Trending (past week)</a
                      >
                    </div>
                  </div>
                  <button
                    type="button"
                    class="btn btn-outline-secondary btn-sm wbg-button ml-2"
                  >
                    <i
                      class="fas fa-chart-bar fa-lg mr-1"
                      aria-hidden="true"
                    ></i
                    >Show statistics
                  </button>
                  <a
                    target="_blank"
                    href="https://mtt-wb21h.netlify.app/search/#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-print" aria-hidden="true"></i></a
                  ><a
                    target="_blank"
                    href="https://mtt-wb21h.netlify.app/search/#"
                    class="btn btn btn-outline-success btn-sm wbg-button ml-2"
                    ><i class="fa fa-file-excel-o" aria-hidden="true"></i
                  ></a>
                </div>
              </div>
            </div>

            <SearchResultCard
              v-for="result in hits"
              :result="result"
              v-bind:key="result.id"
            />

            <div class="nada-pagination">
              <div
                class="row mt-3 mb-3 d-flex justify-content-lg-between align-items-center"
              >
                <div class="col-12 col-lg-6 mb-3 small">
                  <div
                    id="items-per-page"
                    class="items-per-page light switch-page-size"
                  >
                    <small
                      >Results per page:
                      <span
                        class="wbg-pagination-btn"
                        v-for="size in page_sizes"
                        v-bind:key="size"
                        @click="setSize(size)"
                        >{{ size }}</span
                      >
                    </small>
                  </div>
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-lg-end">
                  <nav aria-label="Page navigation">
                    <ul
                      class="pagination pagination-md wbg-pagination-ul small"
                    >
                      <li
                        class="page-item"
                        v-for="page_num in num_pages"
                        v-bind:key="page_num"
                      >
                        <a
                          @click="sendSearch((page_num - 1) * size)"
                          class="page-link active"
                          :data-page="page_num"
                          >{{ page_num }}</a
                        >
                      </li>

                      <li class="page-item">
                        <a
                          @click="sendSearch(next)"
                          class="page-link"
                          data-page="2"
                          >Next</a
                        >
                      </li>
                      <li class="page-item">
                        <a
                          @click="sendSearch((num_pages - 1) * size)"
                          class="page-link"
                          :data-page="num_pages + 1"
                          title="Last"
                          >»</a
                        >
                      </li>
                    </ul>
                  </nav>
                </div>
              </div>
            </div>
            <hr />
            <footer>
              <section>
                <h4>Share</h4>
                <nav class="nav sharing-icons mt-4">
                  <a
                    class="nav-item"
                    href="https://www.facebook.com/sharer/sharer.php?u=%2fsearch%2f"
                    title="Share on Facebook"
                    ><span
                      class="fab fa-facebook-f fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://www.linkedin.com/shareArticle?mini=true&amp;url=%2fsearch%2f"
                    title="Share on LinkedIn"
                    ><span
                      class="fab fa-linkedin-in fa-lg"
                      aria-hidden="true"
                    ></span></a
                  ><a
                    class="nav-item"
                    href="https://twitter.com/intent/tweet?url=%2fsearch%2f&amp;text=Search"
                    title="Tweet this"
                    ><span
                      class="fab fa-twitter fa-lg"
                      aria-hidden="true"
                    ></span
                  ></a>
                </nav>
              </section>
            </footer>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import $ from "jquery";
import SearchResultCard from "./common/SearchResultCard";

export default {
  name: "Search",
  components: { SearchResultCard },
  mounted() {
    this.flowSideBar();
  },
  computed: {
    searchParams() {
      const params = new URLSearchParams();
      params.append("query", this.query);
      params.append("from_result", this.from_result);
      params.append("size", this.size);
      return params;
    },
    myProps() {
      var retVal = null;
      if (this.$route.name === "a") {
        retVal = { foo: this.foo };
      }
      if (this.$route.name === "b") {
        retVal = { bar: this.bar };
      }
      return retVal;
    },
  },
  data: function () {
    return {
      search_type: "keyword",
      keyword_search_api_url: "/nlp/search/keyword",
      semantic_search_api_url: "/nlp/search/semantic",
      page_sizes: [10, 25, 50, 100],
      start: 0,
      end: 0,
      next: 0,
      num_pages: 0,
      query: "",
      from_result: 0,
      size: 10,
      hits: [],
      total: Object,
      errored: false,
      loading: false,
    };
  },
  methods: {
    resetFrom: function () {
      this.from_result = 0;
    },
    sendSearch: function (from = 0) {
      if (this.search_type == "keyword") {
        this.sendKeywordSearch(from);
      } else if (this.search_type == "semantic") {
        this.sendSemanticSearch(from);
      } else {
        return;
      }
    },
    sendKeywordSearch: function (from = 0) {
      if (from > this.total.value) {
        return;
      }
      this.from_result = from;
      this.loading = true;

      this.$http
        .get(this.keyword_search_api_url, {
          params: this.searchParams,
        })
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = response.data.next;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.size);
          if (this.total.value % this.size > 0) {
            this.num_pages += 1;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },
    sendSemanticSearch: function (from = 0) {
      // if (from > this.total.value) {
      //   return;
      // }
      this.from_result = from;
      this.loading = true;

      this.$http
        .get(this.semantic_search_api_url, {
          params: this.searchParams,
        })
        .then((response) => {
          this.hits = response.data.hits;
          this.total = response.data.total;
          this.next = response.data.next;
          this.start = this.from_result + 1;
          this.end = this.from_result + this.hits.length;
          this.num_pages = Math.floor(this.total.value / this.size);
          if (this.total.value % this.size > 0) {
            this.num_pages += 1;
          }
        })
        .catch((error) => {
          console.log(error);
          this.errored = true;
          this.loading = false;
        })
        .finally(() => (this.loading = false));
    },

    setSize: function (size) {
      this.size = size;
    },
    flowSideBar: function () {
      $(function () {
        var $sidebar = $("#blog-sidebar"),
          $window = $(window),
          offset = $sidebar.offset(),
          topPadding = 15;

        $window.scroll(function () {
          if (($window.scrollTop() > offset.top) & ($(window).width() > 768)) {
            $sidebar.stop().animate(
              {
                marginTop: $window.scrollTop() - offset.top + topPadding,
              },
              { easing: "ease", duration: 0 }
            );
          } else {
            $sidebar.stop().animate({
              marginTop: 0,
            });
          }
        });
      });
    },
  },
};
</script>

<style scoped>
@import "../../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

.content-row {
  min-height: 50vh;
}
@media (min-width: 1200px) {
  .flowing {
    max-width: 1200px;
  }
}

.wbg-internal-header {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

/*
.blog-main {
  margin: 0;
  padding-left: 1rem;
}

.blog-sidebar {
  margin-left: -2rem;
  padding: 0;
} */
</style>