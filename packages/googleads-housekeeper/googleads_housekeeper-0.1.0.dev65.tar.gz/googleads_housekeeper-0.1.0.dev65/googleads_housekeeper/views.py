# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pre-build views for simplifying reads from DB."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

import gaarf
from gaarf import parsers

from googleads_housekeeper.domain.core import preview_task_and_results
from googleads_housekeeper.domain.placement_handler.placement_service import (
  PAGE_SIZE,
)
from googleads_housekeeper.services import unit_of_work

registry = {}


def task(
  task_id: int, uow: unit_of_work.AbstractUnitOfWork
) -> dict[str, Any] | None:
  with uow:
    if uow_task := uow.tasks.get(task_id):
      return asdict(uow_task)
    return None


def tasks(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
  with uow:
    uow_tasks: list[dict[str, Any]] = []
    for uow_task in uow.tasks.list():
      task_dict = uow_task.to_dict()
      task_dict['next_run'] = uow_task.next_run
      accounts = customer_ids(
        uow=uow, accounts=uow_task.customer_ids.split(',')
      )
      task_dict['accounts'] = list({a.get('account_name') for a in accounts})
      if task_executions := executions(uow_task.id, uow):
        for current_execution in sorted(
          task_executions, key=lambda x: x.get('end_time'), reverse=True
        ):
          task_dict['placements_excluded'] = current_execution.get(
            'placements_excluded'
          )
          task_dict['last_run'] = current_execution.get('end_time').strftime(
            '%Y-%m-%d %H-%M'
          )
          break
      else:
        task_dict['placements_excluded'] = None
      uow_tasks.append(task_dict)
    return uow_tasks


def config(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
  with uow:
    return [asdict(c) for c in uow.settings.list()]


def allowlisted_placements(
  uow: unit_of_work.AbstractUnitOfWork, account_id: str | None = None
) -> list[dict] | None:
  with uow:
    if account_id:
      if uow_allowlisted_placements := uow.allowlisting.get_by_conditions(
        {'account_id': account_id}
      ):
        return [asdict(t) for t in uow_allowlisted_placements]
    if uow_allowlisted_placements := uow.allowlisting.list():
      return [asdict(t) for t in uow_allowlisted_placements]
  return None


def allowlisted_placements_as_tuples(
  uow: unit_of_work.AbstractUnitOfWork, account_id: str | None = None
) -> list[tuple[str, str, str]]:
  if placements := allowlisted_placements(uow, account_id):
    return [
      (p.get('account_id'), p.get('type'), p.get('name')) for p in placements
    ]
  return []


def execution(
  execution_id: str, uow: unit_of_work.AbstractUnitOfWork
) -> dict[str, Any] | None:
  with uow:
    if task_execution := uow.executions.get(execution_id):
      return asdict(task_execution)
  return None


def executions(
  task_id: str, uow: unit_of_work.AbstractUnitOfWork
) -> list[dict[str, Any]] | None:
  with uow:
    if task_executions := uow.executions.get_by_condition('task', task_id):
      return [asdict(t) for t in task_executions]
  return None


def execution_details(
  task_id: str,
  execution_id: str,
  uow: unit_of_work.AbstractUnitOfWork,
  first_n_placements: int | None = None,
) -> list[dict[str, Any]] | None:
  with uow:
    if uow.executions.get_by_condition('task', task_id):
      if uow_execution_details := uow.execution_details.get_by_condition(
        'execution_id', execution_id
      ):
        results = [asdict(t) for t in uow_execution_details]
        if first_n_placements and first_n_placements < len(results):
          results = results[:first_n_placements]
        return results
  return None


def customer_ids(
  uow: unit_of_work.AbstractUnitOfWork,
  mcc_id: str | None = None,
  accounts: list[str] | None = None,
) -> list[dict[str, Any]]:
  with uow:
    if mcc_id:
      uow_customer_ids = [
        asdict(r) for r in uow.customer_ids.list() if r.mcc_id == mcc_id
      ]
    elif accounts:
      uow_customer_ids = [
        asdict(r) for r in uow.customer_ids.list() if r.id in accounts
      ]
    else:
      raise ValueError('Neither mcc_id nor accounts were provided')
    return uow_customer_ids


def mcc_ids(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, str]]:
  if registry_mcc_ids := registry.get('mcc_ids'):
    return registry_mcc_ids
  with uow:
    uow_mcc_ids = [asdict(r) for r in uow.mcc_ids.list()]
    registry['mcc_ids'] = uow_mcc_ids
    return uow_mcc_ids


def upsert_async_preview_to_db(
  task_and_results: preview_task_and_results.PreviewTaskAndResults,
  uow: unit_of_work.AbstractUnitOfWork,
):
  with uow:
    existing_task_and_results = uow.preview_task_and_results.get_by_condition(
      'preview_task_id', task_and_results.id
    )

    if existing_task_and_results:
      uow.preview_task_and_results.update(
        task_id=task_and_results.id,
        update_dict={'results': task_and_results.results},
      )
    else:
      uow.preview_task_and_results.add(task=task_and_results)

import json
def _gaarf_from_json(cls, json_str: str) -> 'GaarfReport':
  """Creates a GaarfReport object from a JSON string.

  Args:
      json_str: JSON string representation of the data.

  Returns:
      GaarfReport.

  Raises:
      TypeError: If any value in the JSON data is not a supported type.
      ValueError: If `data` is a list but not all dictionaries
      have the same keys.
  """
  data = json.loads(json_str)

  def validate_value(value):
    if not isinstance(value, parsers.GoogleAdsRowElement):
      raise TypeError(
        f'Unsupported type {type(value)} for value {value}. '
        'Expected types: int, float, str, bool, list, or None.'
      )
    return value

  # Case 1: `data` is a dictionary
  if isinstance(data, dict):
    column_names = list(data.keys())
    if not data.values():
      results = []
    else:
      results = [[validate_value(value) for value in data.values()]]

  # Case 2: `data` is a list of dictionaries, each representing a row
  elif isinstance(data, list):
    column_names = list(data[0].keys()) if data else []
    results = [
      [validate_value(value) for value in row.values()] for row in data
    ]
    for row in data:
      if not isinstance(row, dict):
        raise TypeError('All elements in the list must be dictionaries.')
      if list(row.keys()) != column_names:
        raise ValueError(
          'All dictionaries must have consistent keys in the same order.'
        )
  else:
    raise TypeError(
      'Input JSON must be a dictionary or a list of dictionaries.'
    )

  return cls(results=results, column_names=column_names)


def get_placements_for_specific_preview_task(
  preview_task_id: str,
  uow: unit_of_work.AbstractUnitOfWork,
  preview_pagination_index_zero_based: int | None = None,
  preview_pagination_size: int | None = PAGE_SIZE,
):
  with uow:
    task_and_results = uow.preview_task_and_results.get_by_condition(
      'preview_task_id', preview_task_id
    )
    if not task_and_results or not task_and_results.results:
      return None
    placements = _gaarf_from_json(task_and_results.results)
    if preview_pagination_index_zero_based is not None:
      first_index = (
        preview_pagination_size * preview_pagination_index_zero_based
      )
      last_index = first_index + preview_pagination_size
      placements = gaarf.report.GaarfReport(
        results=placements.results[first_index:last_index],
        column_names=placements.column_names,
      )
  return placements



