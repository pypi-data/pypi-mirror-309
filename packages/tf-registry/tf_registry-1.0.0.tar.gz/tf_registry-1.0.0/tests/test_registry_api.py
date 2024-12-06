# -*- coding: utf-8 -*-

import pytest

from tf_registry import Meta, Metrics, ModuleList, Summary


@pytest.mark.vcr
def test_list(client, snapshot) -> None:
    modules = client.list()

    assert modules == snapshot


@pytest.mark.vcr
def test_list_namespace(client, snapshot) -> None:
    modules = client.list("terraform-aws-modules")

    assert modules == snapshot


@pytest.mark.vcr
def test_search(client) -> None:
    modules = client.search("dokku")

    assert modules == ModuleList(
        meta=Meta(
            limit=15,
            current_offset=0,
            next_offset=None,
            prev_offset=None,
        ),
        modules=[],
    )


@pytest.mark.vcr
def test_versions(client, snapshot) -> None:
    versions = client.versions("terraform-alicloud-modules", "disk", "alicloud")

    assert versions == snapshot


@pytest.mark.vcr
def test_latest(client, snapshot) -> None:
    modules = client.latest("hashicorp", "consul")

    assert modules == snapshot


@pytest.mark.vcr
def test_latest_for_provider(client, snapshot) -> None:
    module = client.latest_for_provider("hashicorp", "consul", "aws")

    assert module == snapshot


@pytest.mark.vcr
def test_get(client, snapshot) -> None:
    module = client.get("hashicorp", "consul", "aws", "0.11.0")

    assert module == snapshot


@pytest.mark.vcr
def test_download_url(client) -> None:
    url = client.download_url("hashicorp", "consul", "aws", "0.11.0")

    assert (
        url == "git::https://github.com/hashicorp/terraform-aws-consul?"
        "ref=e9ceb573687c3d28516c9e3714caca84db64a766"
    )


@pytest.mark.vcr
def test_latest_download_url(client) -> None:
    url = client.latest_download_url("hashicorp", "consul", "aws")

    assert (
        url == "git::https://github.com/hashicorp/terraform-aws-consul?"
        "ref=e9ceb573687c3d28516c9e3714caca84db64a766"
    )


@pytest.mark.vcr
def test_metrics(client) -> None:
    metrics = client.metrics("hashicorp", "consul", "aws")

    assert metrics == Summary(
        data=Metrics(
            type="module-downloads-summary",
            id="hashicorp/consul/aws",
            attributes={"month": 967, "total": 185417, "week": 513, "year": 44981},
        )
    )
