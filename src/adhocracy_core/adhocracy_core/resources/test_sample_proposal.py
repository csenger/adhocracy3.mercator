from pyramid import testing
from pytest import fixture
from pytest import mark


def test_proposalversion_meta():
    from .sample_proposal import proposalversion_meta
    from .sample_proposal import IProposalVersion
    import adhocracy_core.sheets
    meta = proposalversion_meta
    assert meta.iresource is IProposalVersion
    assert meta.extended_sheets == [adhocracy_core.sheets.document.IDocument,
                                    adhocracy_core.sheets.comment.ICommentable
                                    ]
    assert meta.permission_add == 'add_proposalversion'


def test_proposal_meta():
    from .sample_proposal import proposal_meta
    from .sample_proposal import IProposalVersion
    from .sample_proposal import IProposal
    from .sample_proposal import ISection
    from .sample_proposal import IParagraph
    from .comment import add_commentsservice
    from .rate import add_ratesservice
    from .tag import ITag
    meta = proposal_meta
    assert meta.iresource is IProposal
    assert meta.element_types == [ITag,
                                  ISection,
                                  IParagraph,
                                  IProposalVersion,
                                  ]
    assert meta.item_type == IProposalVersion
    assert meta.permission_add == 'add_proposal'
    assert add_commentsservice in meta.after_creation
    assert add_ratesservice in meta.after_creation


@fixture
def integration(config):
    config.include('adhocracy_core.content')
    config.include('adhocracy_core.events')
    config.include('adhocracy_core.catalog')
    config.include('adhocracy_core.sheets')
    config.include('adhocracy_core.resources.sample_proposal')
    config.include('adhocracy_core.resources.tag')
    config.include('adhocracy_core.resources.comment')
    config.include('adhocracy_core.resources.rate')


@mark.usefixtures('integration')
class TestProposal:

    @fixture
    def context(self, pool):
        return pool

    def test_create_proposal(self, context, registry):
        from adhocracy_core.resources.sample_proposal import IProposal
        from adhocracy_core.sheets.name import IName
        appstructs = {IName.__identifier__: {'name': 'name1'}}
        res = registry.content.create(IProposal.__identifier__,
                                      appstructs=appstructs,
                                      parent=context)
        assert IProposal.providedBy(res)

    def test_create_proposalversion(self, context, registry):
        from adhocracy_core.resources.sample_proposal import IProposalVersion
        res = registry.content.create(IProposalVersion.__identifier__,
                                      parent=context)
        assert IProposalVersion.providedBy(res)
