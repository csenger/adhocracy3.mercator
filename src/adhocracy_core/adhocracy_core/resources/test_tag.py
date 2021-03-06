from pyramid import testing
from pytest import fixture
from pytest import mark


def test_tag_meta():
    from .tag import tag_metadata
    from .tag import ITag
    import adhocracy_core.sheets
    meta = tag_metadata
    assert meta.iresource is ITag
    assert meta.basic_sheets==[adhocracy_core.sheets.name.IName,
                               adhocracy_core.sheets.metadata.IMetadata,
                               adhocracy_core.sheets.tags.ITag,
                               ]
    assert meta.permission_add == 'add_tag'


@fixture
def integration(config):
    config.include('adhocracy_core.content')
    config.include('adhocracy_core.events')
    config.include('adhocracy_core.catalog')
    config.include('adhocracy_core.sheets')
    config.include('adhocracy_core.resources.tag')


@mark.usefixtures('integration')
class TestTag:

    @fixture
    def context(self, pool):
        return pool

    def test_create_tag(self, context, registry):
        from adhocracy_core.resources.tag import ITag
        from adhocracy_core.sheets.name import IName
        appstructs = {IName.__identifier__: {'name': 'name1'}}
        res = registry.content.create(ITag.__identifier__,
                                      appstructs=appstructs,
                                      parent=context)
        assert ITag.providedBy(res)
