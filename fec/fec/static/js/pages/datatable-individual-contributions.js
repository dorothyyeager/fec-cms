'use strict';

var $ = require('jquery');

var tables = require('../modules/tables');
var helpers = require('../modules/helpers');
var columns = require('../modules/columns');

var donationTemplate = require('../templates/receipts.hbs');

$(document).ready(function() {
  var $table = $('#results');
  new tables.DataTable($table, {
    autoWidth: false,
    title: 'Individual contributions',
    path: ['schedules', 'schedule_a'],
    query: {is_individual: true},
    columns: columns.individualContributions,
    paginator: tables.SeekPaginator,
    order: [[4, 'desc']],
    useFilters: true,
    useExport: true,
    rowCallback: tables.modalRenderRow,
    callbacks: {
      afterRender: tables.modalRenderFactory(donationTemplate)
    }
  });
});
